import os
import platform
import subprocess
import threading

class SubprocessRunner:
    def __init__(self, script_path):
        self.script_path = script_path

    def run_script(self):
        # Start the process without redirecting stderr
        process = subprocess.Popen(self.script_path, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, shell=True, start_new_session=True)
        
        # Wait for the process to complete and capture stdout and stderr
        _, stderr = process.communicate()
        
        # Check if there were any errors
        if stderr:
            print("Errors encountered:")
            print(stderr.decode())  # Decoding from bytes to string for readability

class PipeHandler:
    def __init__(self, pipe_path):
        self.pipe_path = pipe_path

    def create_pipe(self):
        if platform.system() == 'Windows':
            import win32pipe
            import win32file

            self.handle = win32pipe.CreateNamedPipe(
                self.pipe_path,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1,
                65536,
                65536,
                0,
                None
            )
          
            win32pipe.ConnectNamedPipe(self.handle, None)
            print("Pipe Connected")

        else:
            if not os.path.exists(self.pipe_path):
                os.mkfifo(self.pipe_path)

            self.handle = open(self.pipe_path, "w+")

    def close_pipe(self):
        if platform.system() == 'Windows':
            import win32file
            win32file.CloseHandle(self.handle)
        else:
            self.handle.close()
            os.remove(self.pipe_path)

    def write_to_pipe(self, message):
        if platform.system() == 'Windows':
            import win32file
            win32file.WriteFile(self.handle, message.encode())
        else:
            self.handle.write(message)
            self.handle.flush()

    def read_from_pipe(self, size=100):
        if platform.system() == 'Windows':
            import win32file
            _, data = win32file.ReadFile(self.handle, size)
            return data.decode()
        else:
            return self.handle.read(size)

if __name__ == "__main__":
    script_path = None
    if platform.system() == 'Windows':
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'executePipeProcess.bat'))
    else:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'executePipeProcess.sh'))

    pipe_path = None
    if platform.system() == 'Windows':
        pipe_path = r'\\.\pipe\my_pipe'
    else:
        pipe_path = "my_pipe"

    subprocess_runner = SubprocessRunner(script_path)
    pipe_handler = PipeHandler(pipe_path)

    print("invoking runscript")
    thread = threading.Thread(target=subprocess_runner.run_script)
    thread.start()

    try:
        pipe_handler.create_pipe()

        message = "Hello from Python!"
        pipe_handler.write_to_pipe(message)

        data = pipe_handler.read_from_pipe()
        print(data)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        pipe_handler.close_pipe()
