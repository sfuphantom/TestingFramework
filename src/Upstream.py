import socket
import threading
import time

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


if __name__ == "__main__":
    communicator = DataCommunicator('127.0.0.1', 8080, 8081)

    # Start listener thread
    communicator.start_listener_thread()

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
        communicator.listener_thread.join(timeout = 3)


