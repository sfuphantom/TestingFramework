#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
    #include <windows.h>
    #define OS_Windows
#else
    #include <unistd.h>
    #include <fcntl.h>
    #define OS_Linux
#endif

#define BUFFFER_SIZE 100

// Structure to hold platform-specific pipe data
typedef struct {
    #ifdef OS_Windows
        HANDLE handle;
    #else
        int fd;
    #endif
} Pipe;

// Function to connect to the named pipe
Pipe connect_to_pipe(const char *pipe_path) {
    Pipe pipe;
    #ifdef OS_Windows
        pipe.handle = CreateFile(
            pipe_path,
            GENERIC_READ | GENERIC_WRITE,
            0,
            NULL,
            OPEN_EXISTING,
            0,
            NULL
        );
        if (pipe.handle == INVALID_HANDLE_VALUE) {
            fprintf(stderr, "Error opening pipe: %d\n", GetLastError());
            exit(EXIT_FAILURE);
        }
    #else
        pipe.fd = open(pipe_path, O_RDWR);
        if (pipe.fd == -1) {
            perror("Error opening pipe");
            exit(EXIT_FAILURE);
        }
    #endif
    return pipe;
}

// Function to read from the named pipe
int read_from_pipe(Pipe pipe, char *buffer, int buffer_size) {
    #ifdef OS_Windows
        DWORD bytes_read;
        BOOL success = ReadFile(pipe.handle, buffer, buffer_size, &bytes_read, NULL);
        if (!success || bytes_read == 0) {
            fprintf(stderr, "Error reading from pipe: %d\n", GetLastError());
            return -1;
        }
        return bytes_read;
    #else
        int bytes_read = read(pipe.fd, buffer, buffer_size);
        if (bytes_read == -1) {
            perror("Error reading from pipe");
            return -1;
        }
        return bytes_read;
    #endif
}

// Function to write to the named pipe
int write_to_pipe(Pipe pipe, const char *data, int data_size) {
    #ifdef OS_Windows
        DWORD bytes_written;
        if (!WriteFile(pipe.handle, data, data_size, &bytes_written, NULL)) {
            fprintf(stderr, "Error writing to pipe: %d\n", GetLastError());
            return -1;
        }
        return bytes_written;
    #else
        int bytes_written = write(pipe.fd, data, data_size);
        if (bytes_written == -1) {
            perror("Error writing to pipe");
            return -1;
        }
        return bytes_written;
    #endif
}

// Function to close the named pipe
void close_pipe(Pipe pipe) {
    #ifdef OS_Windows
        CloseHandle(pipe.handle);
    #else
        close(pipe.fd);
    #endif
}

int main() {
    const char *pipe_path = "\\\\.\\pipe\\my_pipe";
    Pipe pipe = connect_to_pipe(pipe_path);

    // Read data from the pipe
    char buffer[BUFFFER_SIZE];
    int bytes_read = read_from_pipe(pipe, buffer, sizeof(buffer));
    if (bytes_read == -1) {
        close_pipe(pipe);
        exit(EXIT_FAILURE);
    }
    if (bytes_read > BUFFFER_SIZE)
    {
        buffer[BUFFFER_SIZE-1] = '\0';
    }
    else
    {
        buffer[bytes_read-1] = '\0';
    }
    // Print the received message
    printf("Received message: %s\n", buffer);

    // Write acknowledgment message to the pipe
    const char *ack_message = "Data from C";
    int bytes_written = write_to_pipe(pipe, ack_message, strlen(ack_message));
    if (bytes_written == -1) {
        close_pipe(pipe);
        exit(EXIT_FAILURE);
    }

    // Write back the received message
    bytes_written = write_to_pipe(pipe, buffer, bytes_read);
    if (bytes_written == -1) {
        close_pipe(pipe);
        exit(EXIT_FAILURE);
    }

    // Close the pipe handle
    close_pipe(pipe);

    return 0;
}
