#!/bin/bash

# Navigate to the source directory
sudo gcc "$(dirname "$0")/archive/PipeCom.C" -o "$(dirname "$0")/archive/pipe.exe"

# Navigate to the output directory
cd "$(dirname "$0")/archive"

# Execute pipe receival from firmware
./pipe.exe
