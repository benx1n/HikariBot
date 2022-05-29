@echo off
echo try to launch the HikarBot
start http://127.0.0.1:8080/go-cqhttp/
cd /d %~dp0
nb run
pause