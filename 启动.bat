@echo off
set PATH=%~dp0pyenv\Library\bin;%~dp0pyenv;%PATH%
if exist %~dp0\pyenv (
    set PLAYWRIGHT_BROWSERS_PATH=0
)

cd /d %~dp0
if not exist .env.prod (
    goto nofile
)

:start
echo try to launch the HikariBot
start http://127.0.0.1:8080/go-cqhttp/
python -m nb_cli run
pause
goto:eof

:nofile
echo Please prepare a .env.prod file first!
echo Exiting..
pause
