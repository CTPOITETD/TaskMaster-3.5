@echo off
setlocal
cd /d "%~dp0"

reg add "HKCU\Software\Classes\.task" /ve /t REG_SZ /d "TaskMaster.Project" /f >nul
reg add "HKCU\Software\Classes\TaskMaster.Project\DefaultIcon" /ve /t REG_SZ /d "%cd%\icon.ico" /f >nul
reg add "HKCU\Software\Classes\TaskMaster.Project\shell\open\command" /ve /t REG_SZ /d "\"%~f0\" \"%%1\"" /f >nul

if "%~1" == "" (
    py TaskMaster.py
) else (
    py TaskMaster.py "%~1"
)

exit