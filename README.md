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



<p align="center">
  <a href="https://pypi.python.org/pypi/hikari-bot">
    <img src="https://img.shields.io/pypi/v/hikari-bot" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8.0+-blue" alt="python">
  <a href="https://jq.qq.com/?_wv=1027&k=S2WcTKi5">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-967546463-orange?style=flat-square" alt="QQ Chat Group">
  </a>
  <a href="https://qun.qq.com/qqweb/qunpro/share?_wv=3&_wwv=128&appChannel=share&inviteCode=1W4NX2S&from=181074&biz=ka#/pc">
    <img src="https://img.shields.io/badge/QQ%E9%A2%91%E9%81%93-yuyuko助手-5492ff?style=flat-square" alt="QQ Channel">
  </a>

# 💘您不打算给可爱的Hikari点个Star吗QAQ
</p>
</div>

## 简介

战舰世界水表BOT，基于Nonebot2  
水表人，出击！wws me recent！！！  
QQ频道官方机器人已上线，请点击上方链接加入体验~  
[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)


## 特色

- [x] 账号总体、单船、近期战绩
- [x] 全指令支持参数乱序
- [x] 快速切换绑定账号
- [x] 实时推送对局信息
- [x] 支持@快速查询
- [x] 全异步，高并发下性能更优
- [x] 支持频道（非官方bot类型）

  <details>
  <summary>点我查看功能列表</summary>

  - 绑定账号：wws bind/set/绑定 [服务器+游戏昵称]：
  - 查询账号绑定列表：wws [查询/查]绑定/绑定列表 [me/@群友]：
  - 切换删除绑定账号：wws [切换/删除]绑定 [序号]
  - 查询账号总体战绩：wws [(服务器+游戏昵称)/@群友/me]
  - 查询账号历史记录：wws [(服务器+游戏昵称)/@群友/me] record
  - 查询账号近期战绩：wws [(服务器+游戏昵称)/@群友/me] recent [日期]
  - 查询单船总体战绩：wws [(服务器+游戏昵称)/@群友/me] ship [船名]
  - 查询单船近期战绩：wws [(服务器+游戏昵称)/@群友/me] ship [船名] recent [日期]
  - 查询服务器排行榜：wws [服务器+战舰名] rank/ship.rank
  - 查询军团详细信息：wws [(服务器+军团名)/@群友/me] clan
  - 查询军团历史记录：wws [(服务器+军团名)/@群友/me] clan record
  - 查询舰船中英文名：wws [搜/查船名] [国家][等级][类型]
  - 检查版本更新：wws 检查更新
  - 更新：wws 更新Hikari
  - 查看帮助：wws help
  - 噗噗：一言

  </details>
  <details>
  <summary>点我查看与Hoshino版的区别</summary>

  - Hikari所使用的Nonebot2框架相比Hoshino更易部署，且两者在单环境下不兼容
  - 一些功能比如频道目前仅支持Hikari
  - Hoshino的插件生态更偏向PCR，具体可以查看[Nonebot2商店](https://v2.nonebot.dev/store)和[Hoshino插件索引](https://github.com/pcrbot/HoshinoBot-plugins-index)
  - 由于个人精力原因，主要功能开发和维护面向Hikari，Hoshino版仅做最低限度功能适配

  </details>
  <details>
  <summary>点我查看遇到问题如何解决</summary>

  - [ ] 请确认您已按文档中部署流程进行
  - [ ] 请确认您已完整浏览[可能会遇到的问题](https://github.com/benx1n/HikariBot#%E5%8F%AF%E8%83%BD%E4%BC%9A%E9%81%87%E5%88%B0%E7%9A%84%E9%97%AE%E9%A2%98)，且仍无法自行解决
  - [ ] [提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)
  - [ ] 提供系统环境和bot版本，以及出现问题前后至少 10 秒的完整日志内容。请自行删除日志内存在的个人信息及敏感内容

  </details>
## 在Windows系统上快速部署
>点我查看[视频教程](https://www.bilibili.com/video/BV1r5411X7pr)

  `windows安装python版本请勿大于3.11,建议版本3.9`

1. 下载Hikari的[最新Release](https://github.com/benx1n/HikariBot/releases/download/Latest/release_windows.zip)并解压到合适文件夹
2. 复制一份`.env.prod-example`文件，并将其重命名为`.env.prod`,打开并按其中注释编辑
    >只显示了.env，没有后面的后缀？请百度`windows如何显示文件后缀名`
    ```
    API_TOKEN = xxxxxxxx #无需引号，TOKEN即回复您的邮件所带的一串由[数字+冒号+英文/数字]组成的字符串
    SUPERUSERS=["QQ号"]
    ```
   - 最后TOKEN应该长这样 `API_TOKEN = 123764323:ba1f2511fc30423bdbb183fe33`
   - 从0.3.2.2版本开始，您没有填写的配置将按.env文件中的默认配置执行，具体逻辑为
      - 私聊、频道默认禁用
      - 群聊默认开启，默认屏蔽官方交流群
      - 默认WEB登录账号密码为admin/admin，如有需要请自行修改，无需设置密码请删除env.prod中的配置项

3. 双击`启动.bat`
    - 页面加载不出请尝试刷新一下，已知IE浏览器可能存在一些问题
    - 此时若没有报错，您可以在打开的页面`http://127.0.0.1:8080/go-cqhttp/`中
      点击左侧添加账号，重启bot即可在网页上看到相应信息（大概率需要扫码）
    - 如果重启后go-cqhhtp一直卡在扫码或无限重启，请跳转[无法使用内嵌go-cqhttp登录](https://github.com/benx1n/HikariBot#%E6%97%A0%E6%B3%95%E4%BD%BF%E7%94%A8%E5%86%85%E5%B5%8Cgo-cqhttp%E7%99%BB%E5%BD%95bot)

## Linux一键脚本
> 仅支持Debian、CentOS、Ubuntu
```
wget -qO - http://www.dddns.icu/installHikari.sh | bash
```


## 使用Docker部署
- Docker目录下是一个简单的Dockerfile，可以基于官方的Python容器封装一个完整的HikariBot
  - 以`12hydrogen/hikari-bot:latest`上线官方仓库
- 注意需要将内部的8080端口映射出来
  ```
  docker run -d -P 12hydrogen/hikari-bot:latest -t [token] -i [qqid] # 首次使用需输入token和qqid，-P表示将8080端口随机映射至主机
  docker run -d -p 12345:8080 12hydrogen/hikari-bot:latest -t [token] -i [qqid] # 使用-p以指定映射在外的端口
  ```
- 运行上述指令后会在终端显示一串字符，即Docker容器的标识符，一般使用前几位即可唯一确定一个容器
  ```
  1a2b3c4d5e..... # 标识符
  docker stop 1a2b # 使用前四位确定，stop即停止容器
  1a2b3c4d5e.....
  docker start 1a2b # start即启动容器
  1a2b3c4d5e.....
  docker restart 1a2b # restart即重启容器
  1a2b3c4d5e.....
  ```
- 在更新后即上传新版本容器
  ```
  docker pull 12hydrogen/hikari-bot:latest # 更新
  docker stop 1a2b
  1a2b...
  docker run -d --volumes-from 1a2b -P 12hydrogen/hikari-bot:latest -t [token] -i [qqid] # 随机映射
  or
  docker run -d --volumes-from 1a2b -p 12345:8080 12hydrogen/hikari-bot:latest -t [token] -i [qqid] # 指定映射
  9z8y... # 注意标识符变化了
  docker rm 1a2b # 删除旧容器，
  1a2b...
  ```
- 将配置文件与容器分离
  使用volume在宿主机保存相关账号信息，更新时按照相关步骤继承volume即可

## 在Windows系统上完整部署
1. 下载[Git](https://git-scm.com/download/win)、[Python](https://www.python.org/downloads/windows/)并安装
    >Python版本需>3.8，或参考[Hoshino版插件](https://github.com/benx1n/wows-stats-bot)中使用Conda虚拟环境
    >
    >请注意python安装时勾选或点击`添加到环境变量`，可以安装后cmd中输入`python --version`来验证是否成功
    >
    >否则请自行百度如何添加python到环境变量

3. 打开一个合适的文件夹，鼠标右键——Git Bash here，输入以下命令（任选一条）克隆本Hikari仓库
    ```
    git clone https://github.com/benx1n/HikariBot.git

    git clone https://gitee.com/benx1n/HikariBot.git
    ```
3. 以管理员身份运行`一键安装.bat`
    >等效于在cmd中执行如下代码
    ```
    python -m pip install nb-cli hikari-bot nonebot-plugin-apscheduler nonebot-plugin-gocqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

4. 复制一份`.env.prod-example`文件，并将其重命名为`.env.prod`,打开并按其中注释编辑
    >只显示了.env，没有后面的后缀？请百度`windows如何显示文件后缀名`
    ```
    API_TOKEN = xxxxxxxx #无需引号，TOKEN即回复您的邮件所带的一串由[数字+冒号+英文/数字]组成的字符串
    SUPERUSERS=["QQ号"]
    ```
   - 最后TOKEN应该长这样 `API_TOKEN = 123764323:ba1f2511fc30423bdbb183fe33`
   - 从0.3.2.2版本开始，您没有填写的配置将按.env文件中的默认配置执行，具体逻辑为
      - 私聊、频道默认禁用
      - 群聊默认开启，默认屏蔽官方交流群`
      - 默认WEB登录账号密码为admin/admin，如有需要请自行修改，无需设置密码请删除env.prod中的配置项
      - 默认开启噗噗
      - 默认开启缓存上报
      - 默认关闭代理

5. 双击`启动.bat`，在打开的浏览器中添加bot账号密码，重新启动Hikari
    - 页面加载不出请尝试刷新一下，已知IE浏览器可能存在一些问题
    - 此时若没有报错，您可以在打开的页面`http://127.0.0.1:8080/go-cqhttp/`中
      点击左侧添加账号，重启bot即可在网页上看到相应信息（大概率需要扫码）
    - 如果重启后go-cqhhtp一直卡在扫码或无限重启，请跳转[无法使用内嵌go-cqhttp登录](https://github.com/benx1n/HikariBot#%E6%97%A0%E6%B3%95%E4%BD%BF%E7%94%A8%E5%86%85%E5%B5%8Cgo-cqhttp%E7%99%BB%E5%BD%95bot)


## ~~在Linux上完整部署~~
- 需要Python基本环境
- Clone本仓库
- 使用`./manage.sh`，基于原有批处理脚本
- 无参数调用以获取使用帮助
1. `install`
    - 安装必须的依赖与bot本体
2. `update`
    - 更新bot
3. `start [-t/--token] [token] [-i/--id] [qqid]`
    - 运行bot
    - 在当前目录下不存在`.env.prod`的情况下从参数获取token和qqid以创建相应文件，否则直接运行
    - 考虑到使用Linux部署时多数情况下本地不存在图形界面，有风险的向公网开放访问
    - 加入验证机制（listed）


## 作为已有Bot的插件部署（如真寻、Haruka）
1. 如果您已经有了一个基于Nonebot2的机器人（例如真寻），您可以直接
    ```
    pip install hikari-bot
    ```
2. 在bot的bot.py中加入
    ```
    nonebot.load_plugin('nonebot_plugin_htmlrender')
    nonebot.load_plugin('hikari_bot')
    ```
3. 在环境文件中加入以下配置项
    ```
    API_TOKEN = xxxxxxxxxxxx
    SUPERUSERS=["QQ号"]
    private = false                 #开启私聊
    group = true                    #开启群聊
    channel = false                 #开启频道
    all_channel = false             #是否全频道生效，无论此项配置如何，channel_list中的频道一定会开启
    channel_list = []               #频道列表白名单，数组形式，可在控制台中获取相应的channel_id
    ban_group_list = [967546463]    #群列表黑名单，默认屏蔽了开发者交流群
    pupu = true                     #是否开启噗噗
    check_cache = true              #是否开启缓存上报,可降低高峰期延迟,如果错误日志中频繁报错上报url:XXXXXXXX,请关闭此项或配置代理
    proxy_on = false                #是否启用代理
    proxy = http://localhost:7890   #代理地址，如果上面选项开启，这边替换为你本地的
    ocr_on = true                   #是否开启ocr(识图指令)
    ocr_offline = false             #是否只使用hash验证，即设置为true后只能识别服务器已记录的图片，如果群较多(>300)导致响应延迟较高可以开启
    ocr_url = http://mc.youthnp.cn:23338/OCR/           #默认ocr地址，一般不用动
    ```
    >一般来说该文件为.env.dev
    >也有可能是.env.pord，具体需要看.env中是否有指定
4.   重启bot

## 更新
实验性更新指令：`wws 更新Hikari`
请确保在能登录上服务器的情况下使用
以下是旧更新方法
1. 按不同版本
   - Windows一键包：下载最新一键包，复制旧版本中`accounts`文件夹和`env.prod`文件替换至新版文件夹中即可
   - 完整版：以管理员身份运行`更新.bat`或执行`./manage.sh update`
      >等效于在cmd中执行如下代码
      ```
      pip install --upgrade hikari-bot
      git pull
      ```
   - 插件版：在cmd中执行如下代码
      ```
      pip install --upgrade hikari-bot
      ```
2. **对比`.env.prod-example`中新增的配置项，并同步至你本地的`env.prod`**
    - install结束后会打印当前版本
    - 您也可以通过`pip show hikari-bot`查看当前Hikari版本
    - 如果没有更新到最新版请等待一会儿，镜像站一般每五分钟同步
    - 从0.3.2.2版本开始，您没有填写的配置将按.env文件中的默认配置执行，具体逻辑为
      - 私聊、频道默认禁用
      - 群聊默认开启，默认屏蔽官方交流群

## 最近的更新日志

### 22-11-18    v0.3.6  包含配置项更新，请添加`env.prod-example`中新增的配置
- [+]新增噗噗（已于0.3.5.2实装）
- [+]新增OCR（已于0.3.5.5实装）
- [+]新增扫雪统计和圣诞船池检查
- [+]新增国服排行榜
- [#]大幅优化高峰期响应速度（已于0.3.5.3实装）
- [#]Linux下支持微软雅黑(已热更新)

### 22-10-29    v0.3.5.5  添加测试功能OCR，支持图片指令
### 22-10-27    v0.3.5.4  修复一键更新指令bug
### 22-10-26    v0.3.5.3  添加缓存上报机制，修复噗噗误触发的bug
### 22-10-25    v0.3.5.2  新增噗噗
### 22-07-24    v0.3.5  适配nontbo2 v2.0.0rc1  
### 22-07-24    v0.3.4  **配置项及入口文件更新**  请完整拉取最新仓库，并同步添加`env.prod-example`中新增的配置
- 重要更新，完整版安装请拉取最新仓库代码，一键包请下载最新版本
- [+]新增一键更新指令，指令wws 更新Hikari
- [+]新增Linux一键脚本 [@94Bo](https://github.com/94Bo)
- [#]修改部分依赖版本
- [#]大幅改动了模板以适配后续功能
- [#]修改框架
- [#]修改接口url
- [#]修复了没有完全修复的兼容性问题[#11](https://github.com/benx1n/HikariBot/issues/11)
- [#]修改日志输出等级，现在控制台只会打印SUCCESS级以上的日志



### 22-07-14    v0.3.3  积累更新
- [+]新增群聊黑名单，默认屏蔽开发者群"
- [+]docker添加CI/CD构建发布 [@12hydrogen](https://github.com/12hydrogen)
- [#]修复与其他插件的兼容性问题
- [#]更改了请求域名
- [#]修复manage.sh会更改toml的问题
- [#]修复了hoshino排行榜选择船只样式问题
- [#]修复仅打过PVE的单船仍会显示战绩详情的问题
- [#]info适配v4接口
- [+]新增配置项ban_group_list

<details>
<summary><b>更以前的更新日志</b></summary>

### 22-07-05    v0.3.2.2  一些修复
- [#]修复切换、删除绑定的bug
- [#]默认配置改为不启用WEB登陆验证
- [#]修复.bat的环境变量问题 [@94Bo](https://github.com/94Bo)

### 22-07-04    v0.3.2.1  **配置项及入口文件更新**  请完整拉取最新仓库，并同步添加`env.prod-example`中新增的配置
- [+]新增对QQ频道的适配（非官方bot接入，官方版bot已上线yuyuko频道）
- [+]新增自定义开启群聊、私聊、QQ频道
- [+]新增web登录密码
- [+]新增默认配置项
- [+]新增PR彩蛋
- [#]info适配V3接口
- [#]recent显示时间区间

### 22-06-23    v0.3.1  **重要功能更新**
- [+]新增单船近期战绩，可显示每日详细信息，指令`wws ship recent`
- [+]新增docker部署 [@12hydrogen](https://github.com/12hydrogen)
- [#]修复国服特殊字符ID无法查询的bug
- [#]修复船只选择过期后发送数字序号仍被识别的bug

### 22-06-15    v0.3.0.1  **重要功能更新**
- [+]支持显示军团评级颜色
- [#]排行榜内部逻辑改动，现在仅显示前十，不更新将无法使用
- [#]\(hotfix)`wws recent`现在无随机战绩不会显示PR和上方战斗信息

### 22-06-08    v0.2.9.4  **重要功能更新**
- [+]新增单船的服务器排行，显示在`wws ship`的详情页面下
- [#]修复0.2.9后无法启动的bug
- [#]js依赖改为本地
- [#]修改recent样式，不更新可能会导致错位
- [#]优化报错提示

### 22-06-03    v0.2.8  一些修复
- [+]新增删除绑定功能
- [#]修复`wws ship`总览经验和胜率不上色的bug
- [#]修复`wws ship`详情只有单野场均被上色的bug
- [#]修复`wws 查船名`中搜不到德国船的bug

### 22-06-03    v0.2.6  [#]修复`wws recent`胜率颜色的bug

### 22-06-03    v0.2.5  [#]修复`wws recent`击杀显示成命中的bug

### 22-06-03    v0.2.4  **重要功能更新** 否则您将无法使用`wws recent`功能
- [+]全指令在游戏名外带上括号即可强制指定昵称，以适配一些带有空格、特殊字符、指令字符的昵称
- [+]新增特殊绑定，请配合网页端食用，复制后发送给Hikari即可一键绑定
- [+]新增部分报错提示
- [#]更改ship,rank,recent样式，现在没有战斗场次的类型不会被显示
- [#]优化Hikari的部署流程
- [#]修复me大写不被识别的问题


### 22-06-02    v0.2.3  一些修复
- [+]全指令支持大写
- [#]修复Linux上可能出现的报错
- [#]修改部分图片的样式

### 22-06-01    v0.2.2  修复了一个VSC导致的依赖错误

### 22-06-01    v0.2.1  修复问题

### 22-06-01    v0.2.0  **重要功能更新**
- [+]新增排位数据
- [+]支持国服
- [+]单船战绩显示单野、自行车、三轮车
- [+]启用gzip，试图改善请求Timeout
- [+]增加3s指令CD和每日100次上限
- [#]修复图片内字符不对称的bug（强迫症）
- [#]修改未绑定账号时的返回
- [#]修复网络问题与找不到游戏名时相同返回的bug
- [#]适配HarukaBot


### 22-05-31    v0.1.9  一些修复
- [#]解决由于QQ风控导致的船只选择列表无法发送的问题
- [#]修复带非me/@参数查询绑定时引起的报错

### 22-05-30    v0.1.8  **重要更新**
- [+]所有带请求参数的部分添加log输出以方便查找问题
- [+]添加平台报错时返回以和Hikari内部错误区分
- [#]移除bat脚本中的utf8以支持部分英文服务器
- [#]试图减少因网络导致的报错问题

### 22-05-30    v0.1.7  一些修复
- [#]修复排行榜查询报错
- [#]修复部分环境可能出现的单船查询无法选择问题

### 22-05-28    v0.1.6  **重要功能更新**
- [+]新增排行榜查询 指令`wws rank/ship.rank`
- [+]新增是否开启内置go-cqhttp，默认开启

### 22-05-28    v0.1.5  一些功能更新
- [+]添加等级显示，适配新舰船数据
- [+]新增wws 检查更新
- [+]配置项添加Bot管理员
- [#]修复定时任务不触发的bug

### 22-05-27    v0.1.4  一些功能优化
- [+]添加在windows下的一键安装、更新、启动脚本
- [#]修复数字ID的recent匹配问题
- [#]优化提示逻辑

### 22-05-27    v0.1.3  一些修复和适配
- [+]适配包括真寻等大部分Nonebot2机器人
- [#]修复自动更新的bug

### 22-05-27    v0.1.2  **调整info接口，不更新无法使用**

### 22-05-27    v0.1.1  一些小改动

### 22-05-27    v0.1.0  一些更新
- [+]新增定时检查更新
- [+]新增部署教程
- [+]添加11级战绩信息
- [#]优化账号总体和单船图片样式

</details>

## 可能会遇到的问题

### go-cqhttp扫码后提示异地无法登录
- 一般提示需要扫码，扫码后提示异地无法登录
- 关于该问题，您可以查看[这里](https://github.com/Mrs4s/go-cqhttp/issues/1469)获得相应解决办法，这里简单列举三种办法
  - 启动时登录方式选择`浏览器滑条`，按后续提示登录
  - 手机下载`爱加速`等代理，连接到服务器对应市级地区
  - 在本地电脑使用go-cqhttp登录成功后，将会在exe同级目录下生成`session.token`和`device.json`两个文件
  将这两个文件复制到服务器对应目录下并重启
    - 内嵌go-cqhttp为`account\QQ号`
    - 独立go-cqhttp为exe所在同级目录下，请注意使用独立go-cqhttp时需要将`.env.prod`的`USE_PLUGIN_GO_CQHTTP`的值改为`false`

### 无法使用内嵌go-cqhttp登录bot

1. 下载 go-cqhttp 至合适的文件夹

    - github 发布页：https://github.com/Mrs4s/go-cqhttp/releases

    > 您需要根据自己的机器架构选择版本，Windows一般为x86/64架构，通常选择[go-cqhttp_windows_386.exe](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_386.exe)

2. 双击go-cqhttp，提示释出bat，重新运行bat，选择websocket反向代理，go-cqhttp将会在同文件夹内自动创建一个`config.yml`，右键使用notepad++打开，根据注释填写QQ账号密码，并将以下内容写入文件结尾（需替换原有的ws-reverse节点）：

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
5. 在文件夹下打开终端，输入`python bot.py`启动bot
    - 一键包双击`启动.bat`即可


### 出现ZoneInfoNotFoundError报错
>
>您可以在[这里](https://github.com/nonebot/nonebot2/issues/78)找到相关解决办法
>
### Recent和绑定提示'鉴权失败'
1. 检查Token是否配置正确，token格式为`XXXXX:XXXXXX`
2. 如果配置正确可能是Token失效了，请重新申请

### 'Config' Object has no attribute XXXX
1. 检查视力，重新阅读[更新](https://github.com/benx1n/HikariBot#更新)章节

### Failed to import "nonebot_plugin_guild_patch"
以下方法任选一种
- 更新python版本至3.9+
- 降低Hikari版本至3.1，等待后续版本修复
- 使用Hikari一键包，其中自带了3.10的python虚拟环境
- 修改依赖包代码，见[这里](https://github.com/mnixry/nonebot-plugin-guild-patch/pull/6/files)

### Ubuntu系统下部署字体不正常(针对一些云服务器的Ubuntu镜像，不保证成功，只是提供一个解决方案)
  1. 执行以下命令，完善字体库并将中文设置成默认语言（部分Ubuntu可能不需要该步骤，可直接从第二步开始）
  ```
  sudo apt install fonts-noto  
  sudo locale-gen zh_CN zh_CN.UTF-8  
  sudo update-locale LC_ALL=zh_CN.UTF-8 LANG=zh_CN.UTF-8  
  sudo fc-cache -fv
  ```
  
  2. 在你的Windows电脑上打开`C:\Windows\fonts`文件夹，找到里面的微软雅黑字体，将其复制出来，放在任意目录，应该会得到`msyh.ttc`，`mshybd.ttc`，`msyhl.ttc`三个文件。（不会有人还用Win7吧？）

  3. 进入到`/usr/share/fonts`文件夹下，创建一个文件夹命名为`msyh`，然后进入其中
  ```
  cd /usr/share/fonts 
  sudo mkdir msyh 
  cd msyh
  ```
  
  4. 将三个字体文件上传到`msyh`文件夹中(过程中遇到的问题请自行解决)

  5. 执行以下命令（此时你应该是在`msyh`文件夹下），加载字体
  ```
  sudo mkfontscale 
  sudo mkfontdir 
  sudo fc-cache -fv
  ```
  
  6. （可选，若不正常可尝试）重启Hikari。

### 首次启动时plugin-gocqhttp的startup方法报错(traceback中一般还有ssl的错误)

1. 下载 go-cqhttp

    - github 发布页：https://github.com/Mrs4s/go-cqhttp/releases

    > 您需要根据自己的机器架构选择版本，Windows一般为x86/64架构，通常选择[go-cqhttp_windows_386.exe](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_386.exe)

2. 重命名为`go-cqhttp.*`(*为所选择版本后缀,如windowx就是go-cqhttp.exe)并放入`HikariBot\accounts\binary`文件夹下

3. 重新启动Hikari


## 贡献

感谢以下开发者及项目做出的贡献与支持

<a href="https://github.com//benx1n/HikariBot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=benx1n/HikariBot" />
</a>

[Nonebot2](https://github.com/nonebot/nonebot2)  
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[战舰世界API平台](https://wows.shinoaki.com/)  

## 开源相关
MIT
修改、分发代码时请保留原作者相关信息
