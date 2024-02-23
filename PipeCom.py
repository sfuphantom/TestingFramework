import os
import platform
import time

if platform.system() == "Windows":
    import win32pipe
    import win32file

    pipe_path = r'\\.\pipe\my_pipe'
    # Create the named pipe
    handle = win32pipe.CreateNamedPipe(
        pipe_path,
        win32pipe.PIPE_ACCESS_OUTBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1,  # Number of instances
        65536,  # Out buffer size
        65536,  # In buffer size
        0,  # Timeout
        None  # Security attributes
    )

    print("what")

    # Connect to the named pipe
    win32pipe.ConnectNamedPipe(handle, None)

    # Write the message to the named pipe
    win32file.WriteFile(handle, b"Hello from Python!")

    # Keep the named pipe open for a short duration
    time.sleep(1)

    # Close the named pipe
    #win32file.CloseHandle(handle)
else:
    pipe_path = "my_pipe"
    # Create the named pipe (FIFO)
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    # Open the pipe for writing
    with open(pipe_path, "w") as pipe:
        message = "Hello from Python!"
        pipe.write(message)

    # Keep the named pipe open for a short duration
    time.sleep(1)

    # Remove the named pipe (optional)
    os.remove(pipe_path)
