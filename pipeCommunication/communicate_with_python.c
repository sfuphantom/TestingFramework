#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

#define BUFFER_SIZE 512

int main() {
    const char *pipe_name = "\\\\.\\pipe\\my_pipe";

    // Create the named pipe for reading
    HANDLE pipe_handle = CreateNamedPipe(
        pipe_name,
        PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES,
        BUFFER_SIZE,
        BUFFER_SIZE,
        0,
        NULL
    );

    if (pipe_handle == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Error creating named pipe: %d\n", GetLastError());
        exit(EXIT_FAILURE);
    }

    printf("Waiting for Python to connect...\n");

    // Wait for Python to connect
    if (!ConnectNamedPipe(pipe_handle, NULL)) {
        fprintf(stderr, "Error connecting to named pipe: %d\n", GetLastError());
        CloseHandle(pipe_handle);
        exit(EXIT_FAILURE);
    }

    printf("Connected to Python\n");

    // Read from the pipe
    char buffer[BUFFER_SIZE];
    DWORD bytes_read;
    while (1) {
        if (!ReadFile(pipe_handle, buffer, BUFFER_SIZE, &bytes_read, NULL)) {
            fprintf(stderr, "Error reading from pipe: %d\n", GetLastError());
            break;
        }
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            printf("Received from Python: %s\n", buffer);
            // Echo back to Python
            if (!WriteFile(pipe_handle, buffer, strlen(buffer) + 1, &bytes_read, NULL)) {
                fprintf(stderr, "Error writing to pipe: %d\n", GetLastError());
                break;
            }
        }
    }

    // Close the pipe handle
    CloseHandle(pipe_handle);

    return 0;
}
