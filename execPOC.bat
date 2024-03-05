rem @echo off

rem Navigate to the output directory
gcc src/DownstreamUDP.C -o output/rcv.exe -lws2_32

rem Navigate to the output directory
cd output

rem Execute rcv.exe with argument 8080
rcv.exe 8080