@echo off
::编码方式设置为utf-8
chcp 65001
echo 正在启动go-cqhttp和HikariBot
start http://127.0.0.1:8080/go-cqhttp/
cd /d %~dp0
nb run
echo.
pause