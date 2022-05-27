<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://github.com/benx1n/HikariBot"><img src="https://s2.loli.net/2022/05/27/6lsND3dA5GxQjMg.png" alt="Hikari " style="width:200px; height:200px; border-radius:100%" ></a>
</p>

<div align="center">

# Hikari

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
战舰世界水表BOT
<!-- prettier-ignore-end -->

</div>

<p align="center">
  <a href="https://github.com/benx1n/HikariBot">
    <img src="https://img.shields.io/github/license/benx1n/HikariBot" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/hikari-bot">
    <img src="https://img.shields.io/pypi/v/hikari-bot" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8.0+-blue" alt="python">
  <a href="https://jq.qq.com/?_wv=1027&k=S2WcTKi5">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-967546463-orange?style=flat-square" alt="QQ Chat Group">
  </a>
</p>

## 简介

战舰世界水表BOT，基于Nonebot2<br>
水表人，出击！wws me recent！！！<br>
如果觉得本插件还不错的话请点个Star哦~<br>
[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)

## 特色

- [x] 账号总体、单船、近期战绩
- [x] 全指令支持参数乱序
- [x] 快速切换绑定账号
- [x] 支持@快速查询

## 快速部署（作为独立bot）
1. 下载[notepad++](https://notepad-plus-plus.org/downloads/)、[Git](https://git-scm.com/download/win)、[Python](https://www.python.org/downloads/windows/)并安装
    >Python版本需>3.8，或参考[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)中使用Conda虚拟环境

3. 打开一个合适的文件夹，鼠标右键——Git Bash here，输入以下命令克隆本Hoshino仓库
   > ```
   > git clone https://github.com/benx1n/HikariBot.git
   > ```
3. 双击`一键安装.bat` 

   >执行下列两条命令安装nonebot2和hikari-bot插件
   > ```
   > pip install nb-cli
   > pip install hikari-bot
   > ```
   >
4. 编辑.env.prod文件
   > ```
   > API_TOKEN = xxxxxxxx #无需引号，格式为您的KEY:TOKEN,半角冒号相连
   > ```

5. 双击`启动.bat`
    >打开终端，进入HikariBot文件夹下，输入下方命令运行bot
    >```
    >nb run
    >```
    >此时若没有报错，您可以打开http://127.0.0.1:8080/go-cqhttp/
    >
    >点击左侧添加账号，重启bot即可在网页上看到相应信息（大概率需要扫码）

## 快速部署（作为插件）
1. 如果您已经有了一个基于Nonebot2的机器人（例如真寻），您可以直接
    ```
    pip install hikari-bot
    ```
2. 在bot的bot.py中加入
    ```
    nonebot.load_plugin('hikari_bot')
    ```
3. 在环境文件中加入API_TOKEN = xxxxxxxxxxxx
>一般来说该文件为.env.dev
>
>也有可能是.env.pord，具体需要看.env中是否有指定
>
>如果啥都不懂，bot.py里,在`nonebot.init()`下面加上
>```
>config = nonebot.get_driver().config
>config.api_token = "xxxxxxxxxxxx"
>```
>请点击页面顶部链接加群获取Token哦~
>
4. 重启bot

## 更新
双击`更新.bat`

>```
>pip install --upgrade hikari-bot
>```
>install结束后会打印当前版本
>
>您也可以通过pip show hikari-bot查看
>
>如果没有更新到最新版请等待一会儿，镜像站一般每五分钟同步
>
>(插件版无需下列两步)
>```
>cd HikariBot
>
>git pull
>```
## 感谢

[Nonebot2](https://github.com/nonebot/nonebot2)<br>
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)<br>
[战舰世界API平台](https://wows.linxun.link/)<br>

## 开源协议

MIT
