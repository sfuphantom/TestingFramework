#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <stdbool.h>

// Function to connect to the named pipe
HANDLE connect_to_pipe(const char *pipe_path) {
    HANDLE pipe_handle = CreateFile(
        pipe_path,
        GENERIC_READ | GENERIC_WRITE,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (pipe_handle == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Error opening pipe: %d\n", GetLastError());
        exit(EXIT_FAILURE);
    }

    return pipe_handle;
}

// Function to read from the named pipe
bool read_from_pipe(HANDLE pipe_handle, char *buffer, DWORD buffer_size, DWORD *bytes_read) {
    BOOL success = ReadFile(pipe_handle, buffer, buffer_size, bytes_read, NULL);
    if (!success || *bytes_read == 0) {
        fprintf(stderr, "Error reading from pipe: %d\n", GetLastError());
        return false;
    }
    return true;
}

// Function to write to the named pipe
bool write_to_pipe(HANDLE pipe_handle, const char *data, DWORD data_size) {
    DWORD bytes_written;
    if (!WriteFile(pipe_handle, data, data_size, &bytes_written, NULL)) {
        fprintf(stderr, "Error writing to pipe: %d\n", GetLastError());
        return false;
    }
    return true;
}

// Function to close the named pipe
void close_pipe(HANDLE pipe_handle) {
    CloseHandle(pipe_handle);
}

int main() {
    const char *pipe_path = "\\\\.\\pipe\\my_pipe";
    HANDLE pipe_handle = connect_to_pipe(pipe_path);

    // Read data from the pipe
    char buffer[100];
    DWORD bytes_read;
    if (!read_from_pipe(pipe_handle, buffer, sizeof(buffer), &bytes_read)) {
        close_pipe(pipe_handle);
        exit(EXIT_FAILURE);
    }

    // Print the received message
    printf("Received message: %s\n", buffer);

    // Write acknowledgment message to the pipe
    const char *ack_message = "Data from C";
    if (!write_to_pipe(pipe_handle, ack_message, strlen(ack_message))) {
        close_pipe(pipe_handle);
        exit(EXIT_FAILURE);
    }

    // Write back the received message
    if (!write_to_pipe(pipe_handle, buffer, bytes_read)) {
        close_pipe(pipe_handle);
        exit(EXIT_FAILURE);
    }

    // Close the pipe handle
    close_pipe(pipe_handle);

    return 0;
}
