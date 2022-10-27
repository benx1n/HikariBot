@echo off
@rem use pyenv python first
set PATH=%~dp0pyenv\Library\bin;%~dp0pyenv;%PATH%

echo Try to upgrade the latest hikari-bot
cd /d %~dp0
python -m pip install --upgrade hikari-bot
git pull
echo.
pause
