#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // For sleep

#ifdef _WIN32
#include <winsock2.h>
#include <windows.h>
#else
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#endif

#define BUFFER_SIZE 1024

void error(const char *msg) {
    perror(msg);
    exit(1);
}

#ifdef _WIN32
DWORD WINAPI listener_thread(LPVOID arg) {
#else
void *listener_thread(void *arg) {
#endif
    int sockfd = *((int *)arg);
    struct sockaddr_in cli_addr;
    int clilen; // Changed type to int
    char buffer[BUFFER_SIZE];
    int n;

    clilen = sizeof(cli_addr);
    while (1) {
        memset(buffer, 0, BUFFER_SIZE);
        n = recvfrom(sockfd, buffer, BUFFER_SIZE, 0, (struct sockaddr *) &cli_addr, &clilen);
        if (n < 0)
            error("ERROR on recvfrom");
        printf("Received packet from %s:%d\n", inet_ntoa(cli_addr.sin_addr), ntohs(cli_addr.sin_port));
        printf("Data: %s\n", buffer);
    }
    
#ifdef _WIN32
    return 0;
#endif
}

int main(int argc, char *argv[]) {
#ifdef _WIN32
    WSADATA wsaData;
#endif
    int sockfd, portno;
    struct sockaddr_in serv_addr;

    if (argc < 2) {
        fprintf(stderr, "ERROR, no port provided\n");
        exit(1);
    }

#ifdef _WIN32
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        error("Failed to initialize Winsock.");
    }
#endif

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0)
        error("ERROR opening socket");

    memset((char *) &serv_addr, 0, sizeof(serv_addr));
    portno = atoi(argv[1]);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR on binding");

#ifdef _WIN32
    HANDLE thread;
    DWORD threadId;
    thread = CreateThread(NULL, 0, listener_thread, &sockfd, 0, &threadId);
    if (thread == NULL)
        error("ERROR creating thread");
#else
    pthread_t thread;
    if (pthread_create(&thread, NULL, listener_thread, (void *)&sockfd) != 0) {
        error("ERROR creating thread");
    }
#endif

    // Wait for 10 seconds
    sleep(10);

#ifdef _WIN32
    TerminateThread(thread, 0);
    CloseHandle(thread);
#else
    pthread_cancel(thread);
    pthread_join(thread, NULL);
#endif

#ifdef _WIN32
    closesocket(sockfd);
    WSACleanup();
#else
    close(sockfd);
#endif

    return 0;
}
