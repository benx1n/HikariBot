@echo off
::编码方式设置为utf-8
chcp 65001
echo 正在安装nonebot
python -m pip install nb-cli -i https://pypi.doubanio.com/simple/
echo.
echo 正在安装HikariBot
python -m pip install hikari-bot -i https://pypi.doubanio.com/simple/
echo.
pause