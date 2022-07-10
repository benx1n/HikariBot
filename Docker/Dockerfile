FROM python:latest

LABEL author=12hydrogen
LABEL email=da584003729@outlook.com

# Environment arguments for playwright
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

EXPOSE 8080
RUN apt update \
&& apt install -y \
locales \
locales-all \
fonts-noto \
libnss3-dev \
libnss3-tools \
libxss1 \
libasound2 \
libxrandr2 \
libxkbcommon-x11-0 \
libxcomposite-dev \
libatk1.0-0 \
libgtk-3-0 \
libgbm-dev \
libxshmfence1 \
gstreamer1.0-libav \
libatk-bridge2.0-0 \
libcups2-dev \
libdbus-glib-1-2
RUN cd /home \
&& mkdir HikariBot \
&& cd HikariBot \
&& git init \
&& git remote add origin https://github.com/12hydrogen/HikariBot.git \
&& git fetch origin master \
&& git merge origin/master
RUN pip install nb-cli hikari-bot \
&& nb plugin install nonebot-plugin-apscheduler \
&& nb plugin install nonebot-plugin-gocqhttp \
&& playwright install chromium \
&& playwright install firefox

WORKDIR /home/HikariBot
ENTRYPOINT ["./manage.sh", "start"]
CMD ["-t", "123456", "-i", "123456"]
