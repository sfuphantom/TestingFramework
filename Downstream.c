#include <stdio.h>
#include <string.h>

#ifdef _WIN32
    #include <winsock2.h>
    #pragma comment(lib, "ws2_32.lib")
#else
    #include <arpa/inet.h>
    #include <unistd.h>
    typedef int SOCKET;
    typedef struct sockaddr_in SOCKADDR_IN;
    typedef struct sockaddr SOCKADDR;
    #define closesocket(s) close(s)
#endif

#define PORT 8080

void processData(const char* data) {
    // Add your C processing logic here
    printf("Received data in C: %s\n", data);
}

int main() {
    #ifdef _WIN32
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            fprintf(stderr, "Failed to initialize Winsock\n");
            return 1;
        }
    #endif

    int serverSocket, clientSocket;
    SOCKADDR_IN serverAddr, clientAddr;
    int addrLen = sizeof(clientAddr);

    // Create socket
    if ((serverSocket = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("Socket creation failed");
        #ifdef _WIN32
            WSACleanup();
        #endif
        return 1;
    }

    // Initialize server address struct
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    // Bind the socket
    if (bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == -1) {
        perror("Binding failed");
        closesocket(serverSocket);
        #ifdef _WIN32
            WSACleanup();
        #endif
        return 1;
    }

    // Listen for incoming connections
    if (listen(serverSocket, 5) == -1) {
        perror("Listening failed");
        closesocket(serverSocket);
        #ifdef _WIN32
            WSACleanup();
        #endif
        return 1;
    }

    printf("Server listening on port %d...\n", PORT);

    // Accept connection
    if ((clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &addrLen)) == -1) {
        perror("Accepting connection failed");
        closesocket(serverSocket);
        #ifdef _WIN32
            WSACleanup();
        #endif
        return 1;
    }

    char buffer[1024];
    int bytesRead;

    // Receive data from client
    while ((bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0)) > 0) {
        buffer[bytesRead] = '\0'; // Null-terminate the received data
        processData(buffer);
    }

    closesocket(clientSocket);
    closesocket(serverSocket);

    #ifdef _WIN32
        WSACleanup();
    #endif

    return 0;
}
