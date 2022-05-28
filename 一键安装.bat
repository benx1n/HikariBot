@echo off
::编码方式设置为utf-8
chcp 65001
:: 检查是否已安装python
python --version 3>NUL 
if errorlevel 1 goto errorNoPython 

echo 正在安装nonebot和hikari
python -m pip install nb-cli hikari-bot -i https://pypi.doubanio.com/simple/
echo.
echo 安装完成,如果没有报错请运行启动.bat
pause
goto:eof 

:errorNoPython 
echo. 
echo Error^: Python未安装或未被添加到环境变量
pause