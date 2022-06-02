@echo off
echo Try to upgrade the latest hikari-bot
cd /d %~dp0
python -m pip install --upgrade hikari-bot
git pull
echo.
pause