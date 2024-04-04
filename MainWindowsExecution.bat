@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    net session >nul 2>&1
    if %errorlevel% == 0 (
        echo Success: Administrative permissions confirmed.
    ) else (
        echo Failure: Current permissions inadequate.
        goto UACPrompt
    )
    goto Start
:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
:Start
    @echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    net session >nul 2>&1
    if %errorlevel% == 0 (
        echo Success: Administrative permissions confirmed.
    ) else (
        echo Failure: Current permissions inadequate.
        goto UACPrompt
    )
    goto Start
:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
:Start
    REM Adjust the path to your Python script relative to the batch file
    python "%~dp0archive\PipeCom.py"
    pause
