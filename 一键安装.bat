@echo off

python --version 3>NUL 
if errorlevel 1 goto errorNoPython 

echo installing Nonebot and Hikari
python -m pip install nb-cli hikari-bot nonebot-plugin-apscheduler nonebot-plugin-gocqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo Install finish,plaese do next
pause
goto:eof 

:errorNoPython 
echo. 
echo Error^: Python is not install or add to PATH
pause