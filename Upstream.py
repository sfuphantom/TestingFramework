import socket
import threading

class DataCommunicator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.lock = threading.Lock()

    def setup_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if not self.socket:
            self.setup_socket()
        self.socket.connect((self.host, self.port))

    def send_data(self, data):
        if not self.socket:
            raise Exception("Socket not initialized. Call setup_socket() and connect() first.")
        
        with self.lock:
            self.socket.sendall(data)

    def close_connection(self):
        if self.socket:
            self.socket.close()


# Example usage:
if __name__ == "__main__":
    communicator = DataCommunicator('127.0.0.1', 8080)

    # Set up the socket and connect
    communicator.setup_socket()
    communicator.connect()

    # Send data in a separate thread
    data_to_send = "Mock Data"

    communicator.send_data(data_to_send.encode())

    # You can continue doing other work here while the thread sends data

    # Close the connection when done
    communicator.close_connection()
