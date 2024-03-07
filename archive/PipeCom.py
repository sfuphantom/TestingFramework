import os
import platform
import time
import subprocess
import threading

def run_script(script_path):
    subprocess.Popen(script_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, shell=True, start_new_session=True)

def invoke_runscript():
    script_path = None
    if platform.system() == 'Windows':
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'executePipeProcess.bat'))
    else:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'executePipeProcess.sh'))

    if script_path:
        thread = threading.Thread(target=run_script, args=(script_path,))
        thread.start()

def create_pipe():
    if platform.system() == 'Windows':
        import win32pipe
        import win32file

        pipe_path = r'\\.\pipe\my_pipe'

        handle = win32pipe.CreateNamedPipe(
            pipe_path,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1,
            65536,
            65536,
            0,
            None
        )
        invoke_runscript()
        print("invoking runsciprt")
        win32pipe.ConnectNamedPipe(handle, None)
        print("pipe connected")

        return handle

    else:
        pipe_path = "my_pipe"
        if not os.path.exists(pipe_path):
            os.mkfifo(pipe_path)

        return open(pipe_path, "w")

def close_pipe(pipe):
    if platform.system() == 'Windows':
        import win32file
        win32file.CloseHandle(pipe)
    else:
        pipe.close()
        os.remove("my_pipe")

if __name__ == "__main__":
    pipe = None
    try:
        pipe = create_pipe()

        if pipe:
            message = "Hello from Python!"
            if platform.system() == 'Windows':
                import win32file
                win32file.WriteFile(pipe, message.encode())
                _, data = win32file.ReadFile(pipe, 100)
            else:
                pipe.write(message)
                pipe.flush()
                data = pipe.read(100)

            print(data)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if pipe:
            close_pipe(pipe)

