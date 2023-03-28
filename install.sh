#!/bin/bash
set -e
#set -v
# Hikaribot for Linux installation script
#
# See https://github.com/benx1n/HikariBot for more installation.
#
# This script is meant for quick & easy install via:
#   $ wget -qO - https://fastly.jsdelivr.net/gh/benx1n/HikariBot@master/install.sh | bash
# Or
#   $ wget -qO - https://github.com/benx1n/HikariBot/raw/master/install.sh | bash -c sh

#url_bot_py="https://gitee.com/benx1n/HikariBot/raw/master/bot.py"
url_bot_py="https://fastly.jsdelivr.net/gh/benx1n/HikariBot@master/bot.py"
#url_env="https://gitee.com/benx1n/HikariBot/raw/master/.env"
url_env="https://fastly.jsdelivr.net/gh/benx1n/HikariBot@master/.env"
#url_example="https://gitee.com/benx1n/HikariBot/raw/master/.env.prod-example"
url_example="https://fastly.jsdelivr.net/gh/benx1n/HikariBot@master/.env.prod-example"
#url_toml="https://gitee.com/benx1n/HikariBot/raw/master/pyproject.toml"
url_toml="https://fastly.jsdelivr.net/gh/benx1n/HikariBot@master/pyproject.toml"

user="$(id -un 2>/dev/null || true)"
if [ "$user" != 'root' ]; then
    echo Error: this installer needs the ability to run commands as root.
    exit 1
fi

command_exists() {
    command -v "$@" > /dev/null 2>&1
}

get_distribution() {
    lsb_dist=""
    # Every system that we officially support has /etc/os-release
    if [ -r /etc/os-release ]; then
        lsb_dist="$(. /etc/os-release && echo "$ID")"
    fi
    echo "$lsb_dist"
}

download_python_appimage() {
    #url_python_AppImage=$(wget --quiet https://api.github.com/repos/niess/python-appimage/releases -O- | grep browser_download_url | grep python3.9 | grep manylinux2014_x86_64 | sed 's_^.*"\(https.*\)"$_\1_g' | sed 's/github.com/ghdown.obfs.dev/g')
    url_python_AppImage="https://ghdown.obfs.dev/niess/python-appimage/releases/download/python3.9/python3.9.16-cp39-cp39-manylinux2014_x86_64.AppImage"
    if command_exists curl; then
        curl "${url_python_AppImage}" --location --output python.AppImage
    else
        wget -O python.AppImage "${url_python_AppImage}"
    fi
}

lsb_dist=$( get_distribution )
warning="Warning: Only Ubuntu 18.04, 20.04, and 22.04 are officially supported by playwright."
python_source=system
case "$lsb_dist" in
    ubuntu)
        unset warning
        if command_exists lsb_release; then
            dist_version="$(lsb_release --codename | cut -f2)"
        fi
        if [ -z "$dist_version" ] && [ -r /etc/lsb-release ]; then
            dist_version="$(. /etc/lsb-release && echo "$DISTRIB_CODENAME")"
        fi
        case "$dist_version" in
            bionic)
                python_source=appimage
            ;;
            focal)
                python_source=appimage
            ;;
        esac
    ;;
    debian)
        #debian 8 9 not tested yet.
        dist_version="$(sed 's/\/.*//' /etc/debian_version | sed 's/\..*//')"
        if [ "$dist_version" -lt "11" ]; then
            python_source=appimage
        fi
    ;;
    centos|rhel|sles)
        #only centos 8 stream tested
        python_source=appimage
        if [ -z "$dist_version" ] && [ -r /etc/os-release ]; then
            dist_version="$(. /etc/os-release && echo "$VERSION_ID")"
        fi
        if [ "$dist_version" -ge "8" ]; then
            python_source=system
        fi
    ;;
    *)
        if [ -z "$lsb_dist" ]; then
            if is_darwin; then
                echo
                echo "ERROR: Unsupported operating system 'macOS'"
                echo
                exit 1
            fi
        fi
        echo
        echo "ERROR: Unsupported distribution '$lsb_dist'"
        echo
        exit 1
    ;;
esac


mkdir -p /root/HikariBot
cd /root/HikariBot
#get bot entry file fron gitee repo
wget -qO bot.py "${url_bot_py}"
wget -qO .env "${url_env}"
wget -qO .env.prod "${url_example}"
wget -qO pyproject.toml "${url_toml}"

case "$lsb_dist" in
    debian|ubuntu)
        echo 'Acquire::http::Pipeline-Depth 0;' >> /etc/apt/apt.conf
        sed -i 's/security.debian.org/mirrors.ustc.edu.cn\/debian-security/g' /etc/apt/sources.list
        sed -i 's/[a-z]*\.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
        sed -i 's/archive\.ubuntu\.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
        apt update
        apt upgrade -y
        if [ "$python_source" = "system" ]; then
            apt install python3-pip wget -y
            PYTHON=python3
        else
            apt install libfuse2 wget -y
            download_python_appimage
            chmod a+x python.AppImage
            PYTHON=/root/HikariBot/python.AppImage
        fi
    ;;
    centos)
        yum update -y
        yum install -y epel-release fuse fuse-libs wget
        yum install -y atk bash cairo cairo-gobject centos-indexhtml \
          dbus-glib dbus-libs fontconfig freetype gdk-pixbuf2 glib2 glibc \
          gtk2 gtk3 libX11 libX11-xcb libXcomposite libXcursor libXdamage \
          libXext libXfixes libXi libXrender libXt liberation-fonts-common \
          liberation-sans-fonts libffi libgcc libstdc++ libxcb mozilla-filesystem \
          nspr nss nss-util p11-kit-trust pango pipewire-libs zlib
        if [ "$python_source" = "system" ]; then
            yum install python39-pip -y
            PYTHON=python3.9
        else
            download_python_appimage
            chmod a+x python.AppImage
            PYTHON=/root/HikariBot/python.AppImage
        fi
    ;;
    *)
        echo "ERROR: Unsupported distribution '$lsb_dist'"
        exit 1
    ;;
esac

## extract-and-run is buggy with PYTHONPATH
#libfuse may not work in container or paravirtualization
if [ "$python_source" = "appimage" ]; then
    set +e
    $PYTHON --version
    if [ "$?" -ne 0 ]; then
        $PYTHON --appimage-extract
        mv squashfs-root/ /root/HikariBot/pyenv
        PYTHON="/root/HikariBot/pyenv/AppRun"
        chmod a+x "$PYTHON"
    fi
    set -e
    $PYTHON --version
fi

#install python packages
$PYTHON -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
$PYTHON -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
$PYTHON -m pip install nb-cli hikari-bot nonebot-plugin-apscheduler nonebot2[fastapi]
$PYTHON -m pip install nonebot-plugin-gocqhttp nonebot-plugin-reboot
$PYTHON -m playwright install firefox
$PYTHON -m playwright install-deps || \
  apt install locales locales-all fonts-noto libnss3-dev libxss1 \
  libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1\
  libdbus-1-dev libdbus-glib-1-dev -y || true


#add systemd qqbot.service
cat > /root/HikariBot/run.sh << EOF
#!/bin/bash
cd \`dirname \$0\`
wget -qO bot.py "${url_bot_py}"
wget -qO .env "${url_env}"
wget -qO pyproject.toml "${url_toml}"
$PYTHON -m pip install --upgrade hikari-bot
$PYTHON -m pip install --upgrade nonebot-plugin-gocqhttp
exec $PYTHON bot.py
EOF
chmod a+x /root/HikariBot/run.sh

cat > /etc/systemd/system/qqbot.service <<EOF
[Unit]
Description=Nonebot2 with Hikari plugin
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=root
ExecStart=/root/HikariBot/run.sh
TimeoutStopSec=infinity

[Install]
WantedBy=multi-user.target
EOF

#for security reason generate a random password
rstring="$( (top -bn1; date) | md5sum )"
password="${rstring:0:6}"
sed -i "s/^GOCQ_WEBUI_PASSWORD.*$/GOCQ_WEBUI_PASSWORD=$password/" .env.prod
systemctl daemon-reload
systemctl enable qqbot.service
systemctl restart qqbot.service || true
systemctl start qqbot.service || true

IP=$(wget -qO - http://checkip.dyndns.com | grep -oE "[0-9]{1,3}(\.[0-9]{1,3}){3}")
tee help.txt <<EOF
================================================================================
$warning
Done!

HikariBot installed in /root/HikariBot
qqbot.service installed in /etc/systemd/system/qqbot.service
Start with system boot

Edit config file:
  $ vi /root/HikariBot/.env.prov

Restart QQbot:
  $ systemctl restart qqbot

To Disable qqbot.service:
  $ systemctl stop qqbot.service
  $ systemctl disable qqbot.service
  # Then you can run bot in your console
  $ bash /root/HikariBot/run.sh

To complete Hikari installation:
1. add QQ account, visite http://$IP:8080/go-cqhttp/
   username: admin
   password: $password
2. edit config file and add your API KEY
3. systemctl restart qqbot.service

如果您对Linux非常的不熟悉请:
1. 访问http://$IP:8080/go-cqhttp/ 添加QQ账号
   用户名：   admin
   默认密码： $password
   （大部分云服务商默认防火墙设置只开放少量必要端口，你需要设置防火墙才能访问这个端口）
2. 使用例如winscp之类的GUI工具修改云服务器上的配置文件"/root/HikariBot/.env.prov"
   添加api key；在GOCQ_WEBUI_PASSWORD这一行修改web页面密码
   如果8080端口已经占用还需要修改PORT=8080这一行
3. 登录服务器运行 systemctl restart qqbot 命令重启机器人服务。
   或者直接在云服务商的面板上重启整个系统来重启qq机器人。机器人开机自启
   （添加qq账号并扫码等后需要重启bot才能生效）

PS：机器人每次启动前会先更新hikari-bot

This message saved in /root/HikariBot/help.txt.
================================================================================
EOF
