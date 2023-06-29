@echo off

set PYTHON=
set GIT=
set VENV_DIR=.\env


:activate_venv
set PYTHON="%VENV_DIR%\Scripts\Python.exe"
echo venv %PYTHON%
echo Starting MatterMostBot...

:launch
%PYTHON% mybot.py %COMMANDLINE_ARGS%
pause
exit /b

