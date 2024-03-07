#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int main() {
    const char *pipe_path = "\\\\.\\pipe\\my_pipe";
    HANDLE pipe_handle;

    // Open the named pipe for writing
    pipe_handle = CreateFile(
        pipe_path,
        GENERIC_WRITE,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (pipe_handle == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Error opening pipe for writing: %d\n", GetLastError());
        exit(EXIT_FAILURE);
    }

    // Write data to the pipe
    const char *data = "Hello from C!";
    DWORD bytes_written;
    if (!WriteFile(pipe_handle, data, strlen(data), &bytes_written, NULL)) {
        fprintf(stderr, "Error writing to pipe: %d\n", GetLastError());
        CloseHandle(pipe_handle);
        exit(EXIT_FAILURE);
    }

    // Close the pipe handle
    //CloseHandle(pipe_handle);

    return 0;
}
