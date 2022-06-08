<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://github.com/benx1n/HikariBot"><img src="https://s2.loli.net/2022/05/28/SFsER8m6TL7jwJ2.png" alt="Hikari " style="width:200px; height:200px" ></a>
</p>

<div align="center">

# Hikari

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
战舰世界水表BOT
<!-- prettier-ignore-end -->

</div>

<p align="center">
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
[视频教程](https://www.bilibili.com/video/BV1r5411X7pr)
1. [Git](https://git-scm.com/download/win)、[Python](https://www.python.org/downloads/windows/)并安装
    >Python版本需>3.8，或参考[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)中使用Conda虚拟环境
    >
    >请注意python安装时勾选或点击`添加到环境变量`，可以安装后cmd中输入`python --version`来验证是否成功
    >
    >否则请自行百度如何添加python到环境变量

3. 打开一个合适的文件夹，鼠标右键——Git Bash here，输入以下命令（任选一条）克隆本Hikari仓库
   > ```
   > git clone https://github.com/benx1n/HikariBot.git
   >
   > git clone https://gitee.com/benx1n/HikariBot.git
   > ```
3. 以管理员身份运行`一键安装.bat` 

   >执行下列两条命令安装nonebot2和hikari-bot插件
   > ```
   > pip install nb-cli
   > pip install hikari-bot
   > ```
   >
4. 复制一份`.env.prod-example`文件，并将其重命名为`.env.prod`,打开并编辑
   > ```
   > API_TOKEN = xxxxxxxx #无需引号，TOKEN即回复您的邮件所带的一串由[数字+冒号+英文/数字]组成的字符串
   >SUPERUSERS=["QQ号"] 
   > ```
   >总之最后应该长这样
   >
   >API_TOKEN = 123764323:ba1f2511fc30423bdbb183fe33
   >
   >只显示了.env，没有后面的后缀？请百度`windows如何显示文件后缀名`

5. 双击`启动.bat`，在打开的浏览器中添加bot账号密码，重新启动Hikari
    >打开终端，进入HikariBot文件夹下，输入下方命令运行bot
    >```
    >nb run
    >```
    >此时若没有报错，您可以打开http://127.0.0.1:8080/go-cqhttp/
    >
    >点击左侧添加账号，重启bot即可在网页上看到相应信息（大概率需要扫码）
    >
    >如果重启后go-cqhhtp一直卡在扫码或无限重启，请继续往下阅读


## 快速部署（作为插件）
1. 如果您已经有了一个基于Nonebot2的机器人（例如真寻），您可以直接
    ```
    pip install hikari-bot
    ```
2. 在bot的bot.py中加入
    ```
    nonebot.load_plugin('hikari_bot')
    ```
3. 在环境文件中加入
    ```
    API_TOKEN = xxxxxxxxxxxx
    SUPERUSERS=["QQ号"] 
    ```
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
以管理员身份运行`更新.bat`

>```
>pip install --upgrade hikari-bot
>git pull
>```
>对比`.env.prod-example`中新增的配置项，并同步至你本地的`env.prod`
>
>install结束后会打印当前版本
>
>您也可以通过pip show hikari-bot查看
>
>如果没有更新到最新版请等待一会儿，镜像站一般每五分钟同步
>

## 可能会遇到的问题

### go-cqhttp扫码后提示异地无法登录
>一般提示需要扫码，扫码后提示异地无法登录
>
>关于该问题，您可以查看[#1469](https://github.com/Mrs4s/go-cqhttp/issues/1469)获得相应解决办法，这里简单列举两种办法
>
>1. 手机下载`爱加速`等代理，连接到服务器对应市级地区
>2. 在本地电脑使用go-cqhttp登录成功后，复制生成的`session.token`和`device.json`到服务器对应目录下，内嵌go-cqhttp为`account\QQ号`，外置直接将整个本地文件夹拷贝过去即可，请注意使用外置go-cqhttp时需要将`.env.prod`的`USE_PLUGIN_GO_CQHTTP`的值改为`false`
>

### 无法使用内嵌go-cqhttp登录bot

1. 下载 go-cqhttp 至合适的文件夹

    - github 发布页：https://github.com/Mrs4s/go-cqhttp/releases

    > 您需要根据自己的机器架构选择版本，Windows一般为x86/64架构，通常选择[go-cqhttp_windows_386.exe](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_386.exe)

2. 双击go-cqhttp，提示释出bat，重新运行bat，选择websocket反向代理，go-cqhttp将会在同文件夹内自动创建一个`config.yml`，右键使用notepad++打开，根据注释填写QQ账号密码，并将以下内容写入文件结尾：

    ```yaml
      - ws-reverse:
          universal: ws://127.0.0.1:8080/onebot/v11/ws
          reconnect-interval: 5000
          middlewares:
            <<: *default
    ```
    
    > 关于go-cqhttp的配置，你可以在[这里](https://docs.go-cqhttp.org/guide/config.html#%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)找到更多说明。

3. 启动go-cqhttp，按照提示登录。


4. 修改Hikari文件夹下.env.prod中`USE_PLUGIN_GO_CQHTTP`的值为`false`
    ```
    USE_PLUGIN_GO_CQHTTP = false
    ```
5. 在文件夹下打开终端，输入`nb run`启动bot


### 出现ZoneInfoNotFoundError报错
>
>[issue#78](https://github.com/nonebot/nonebot2/issues/78)
>
## 感谢

[Nonebot2](https://github.com/nonebot/nonebot2)<br>
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)<br>
[战舰世界API平台](https://wows.linxun.link/)<br>

## 开源协议

MIT
