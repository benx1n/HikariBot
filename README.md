# HikariBot
战舰世界水表Bot，基于Nonebot2<br>
水表人，出击！wws me recent！！！<br>
如果觉得本插件还不错的话请点个Star哦~<br>
[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)
## 特点

- [x] 账号总体、单船、近期战绩
- [x] 全指令支持参数乱序
- [x] 快速切换绑定账号
- [x] 支持@快速查询

## 快速部署（作为独立bot）
1. 下载[notepad++](https://notepad-plus-plus.org/downloads/)和[Git](https://git-scm.com/download/win)并安装

2. 下载[Python](https://www.python.org/downloads/windows/)版本需>3.8，或参考[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)中使用Conda虚拟环境

2. 执行下列两条命令安装nonebot2和hikari-bot插件
    ```
    pip install nb-cli
    pip install hikari-bot
    ```
3. 打开一个合适的文件夹，鼠标右键——Git Bash here，输入以下命令克隆本Hoshino仓库
    ```
    git clone https://github.com/benx1n/HikariBot.git
    cd HikariBot
    ```
4. 编辑.env.prod文件
    ```
    API_TOKEN = xxxxxxxx #无需引号
    ```
4. 运行bot
    ```
    nb run
    ```
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
3. 重启bot

## 更新

```
pip install --upgrade hikari-bot
cd HikariBot
git pull
```

## 感谢

[Nonebot2](https://github.com/nonebot/nonebot2)<br>
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)<br>
[战舰世界API平台](https://wows.linxun.link/)<br>

## 开源协议

MIT
