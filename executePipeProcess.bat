@echo on

rem Navigate to the source directory
gcc archive/PipeCom.C -o archive/pipe.exe -lws2_32

rem Navigate to the output directory
cd archive

rem Execute pipe receival from firmware
pipe.exe