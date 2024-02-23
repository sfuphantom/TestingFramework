import socket
import threading
import time

class DataCommunicator:
    def __init__(self, host, send_port, listen_port):
        self.host = host
        self.send_port = send_port
        self.listen_port = listen_port
        self.send_socket = None
        self.listen_socket = None
        self.send_lock = threading.Lock()
        self.listen_lock = threading.Lock()

    def setup_send_socket(self):
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_listen_socket(self):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.host, self.listen_port))
        self.listen_socket.listen(1)

    def connect_send_socket(self):
        if not self.send_socket:
            self.setup_send_socket()
        self.send_socket.connect((self.host, self.send_port))

    def connect_listen_socket(self):
        if not self.listen_socket:
            self.setup_listen_socket()
        client_socket, _ = self.listen_socket.accept()
        self.listen_socket = client_socket

    def send_data(self, data):
        if not self.send_socket:
            raise Exception("Send socket not initialized. Call connect_send_socket() first.")

        with self.send_lock:
            self.send_socket.sendall(data.encode())

    def receive_data(self):
        if not self.listen_socket:
            raise Exception("Listen socket not initialized. Call connect_listen_socket() first.")

        with self.listen_lock:
            data = self.listen_socket.recv(1024)
            return data.decode()

    def listen_for_data(self):
        while True:
            received_data = self.receive_data()
            if not received_data:
                break
            print("Received data:", received_data)
            time.sleep(1)  # Adjust as needed

    def close_connection(self):
        if self.send_socket:
            self.send_socket.close()
        if self.listen_socket:
            self.listen_socket.close()

    def send_data_in_thread(self, data):
        thread = threading.Thread(target=self.send_data, args=(data,))
        thread.start()

    def start_listener_thread(self):
        listener_thread = threading.Thread(target=self.listen_for_data)
        listener_thread.start()

# Example usage:
if __name__ == "__main__":
    communicator = DataCommunicator('127.0.0.1', 8080, 8081)

    # Connect sending socket
    communicator.connect_send_socket()

    # Connect receiving socket
    #communicator.connect_listen_socket()

    # Start listener thread
    #communicator.start_listener_thread()

    # Send data in a separate thread
    data_to_send = "Hello from Python in a separate thread!"
    communicator.send_data_in_thread(data_to_send)

    # You can continue doing other work here while the threads run

    # Close the connection when done
    #communicator.close_connection()
