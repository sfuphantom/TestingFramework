#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <io.h>

int main() {
    const char *pipe_path = "\\\\.\\pipe\\my_pipe";
    char buffer[256];

    // Open the named pipe for reading
    int fd = open(pipe_path, O_RDONLY);

    if (fd == -1) {
        perror("Error opening pipe for reading");
        exit(EXIT_FAILURE);
    }

    // Read data from the pipe
    ssize_t bytesRead = read(fd, buffer, sizeof(buffer));
    buffer[bytesRead] = '\0';

    if (bytesRead == -1) {
        perror("Error reading from pipe");
        close(fd);
        exit(EXIT_FAILURE);
    }

    // Print the received message
    printf("Received message: %s\n", buffer);

    // Close the pipe
    close(fd);

    return 0;
}
