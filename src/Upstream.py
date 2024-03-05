import socket
import threading
import time
import os

import subprocess
import platform

class DataCommunicator:
    def __init__(self, host, send_port, listen_port):
        self.host = host
        self.send_port = send_port
        self.listen_port = listen_port
        self.socket = None
        self.lock = threading.Lock()
        self.running = True

    def setup_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.listen_port))

    def send_data(self, data):
        if not self.socket:
            self.setup_socket()

        #with self.lock:
        self.socket.sendto(data.encode(), (self.host, self.send_port))

    def receive_data(self):
        if not self.socket:
            self.setup_socket()

        #with self.lock:
        data, _ = self.socket.recvfrom(1024)
        return data.decode()

    def listen_for_data(self):
        while self.running:
            received_data = self.receive_data()
            if not received_data:
                break
            print("Received data:", received_data)
            time.sleep(1)  # Adjust as needed

    def close_connection(self):
        if self.socket:
            self.socket.close()

    def send_data_in_thread(self, data):
        self.Sendthread = threading.Thread(target=self.send_data, args=(data,))
        self.Sendthread.start()

    def start_listener_thread(self):
        self.listener_thread = threading.Thread(target=self.listen_for_data)
        self.listener_thread.start()

    def stop_threads(self):
        self.running = False


def run_batch_file():
    batch_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'execPOC.bat'))
    subprocess.Popen(batch_file_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

def run_shell_script():
    shell_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'execPOC.sh'))
    subprocess.Popen(['sh', shell_script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

def invoke_runscript():
    if platform.system() == 'Windows':
        batch_thread = threading.Thread(target=run_batch_file)
        batch_thread.start()
    else:
        shell_thread = threading.Thread(target=run_shell_script)
        shell_thread.start()

if __name__ == "__main__":
    communicator = DataCommunicator('127.0.0.1', 8080, 8081)

    # Start listener thread
    communicator.start_listener_thread()

    invoke_runscript()

    try:
        # Send data in a separate thread
        usrinput = ""
        while usrinput != "!":
            usrinput = input(">>>")
            communicator.send_data_in_thread(usrinput)
    except KeyboardInterrupt:
        print("\nExiting due to KeyboardInterrupt...")
    finally:
        # Close the connection when done
        communicator.close_connection()
        communicator.listener_thread.join(timeout=3)