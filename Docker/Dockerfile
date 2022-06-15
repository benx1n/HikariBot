FROM python:latest

LABEL author=12hydrogen
LABEL email=da584003729@outlook.com

# Environment arguments for playwright
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

EXPOSE 8080
RUN apt update \
&& apt install -y locales locales-all fonts-noto libnss3-dev libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1 \
&& cd /home \
&& git clone https://gitee.com/benx1n/HikariBot.git \
&& pip config set global.index-url http://mirrors.tencentyun.com/pypi/simple \
&& pip config set install.trusted-host mirrors.tencentyun.com \
&& pip install nb-cli hikari-bot \
&& nb plugin install nonebot-plugin-apscheduler \
&& nb plugin install nonebot-plugin-gocqhttp \
&& playwright install chromium

WORKDIR /home/HikariBot
ENTRYPOINT ["./manage.sh", "start"]
CMD ["-t", "123456", "-i", "123456"]
