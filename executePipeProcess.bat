@echo on

rem Navigate to the source directory
gcc %~dp0archive\PipeCom.C -o %~dp0archive\pipe.exe -lws2_32

rem Navigate to the output directory
cd %~dp0archive

rem Execute pipe receival from firmware
.\pipe.exe