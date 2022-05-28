@echo off
::编码方式设置为utf-8
chcp 65001
echo 正在获取最新版本HikariBot
python -m pip install --upgrade hikari-bot
echo.
pause