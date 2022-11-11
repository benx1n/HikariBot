FROM python:3.10

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
&& git remote add origin https://github.com/benx1n/HikariBot.git \
&& git config core.sparsecheckout true \
&& echo "!/src" >> ./.git/info/sparsecheckout \
&& echo "!/Docker" >> ./.git/info/sparsecheckout \
&& echo "!/.github" >> ./.git/info/sparsecheckout \
&& echo "!*.bat" >> ./.git/info/sparsecheckout \
&& git pull origin master \
&& rm -rf .git
RUN pip install nb-cli hikari-bot \
&& nb plugin install nonebot-plugin-apscheduler \
&& nb plugin install nonebot-plugin-gocqhttp \
&& playwright install chromium \
&& playwright install firefox
RUN cd /home/HikariBot\
&& mkdir -p accounts/binary \
&& cd accounts/binary \
&& wget -cO temp.tar.gz https://github.com/Mrs4s/go-cqhttp/releases/latest/download/go-cqhttp_linux_amd64.tar.gz \
&& tar xf temp.tar.gz

VOLUME ["/home/HikariBot/accounts"]

WORKDIR /home/HikariBot
ENTRYPOINT ["./manage.sh", "start"]
CMD ["-t", "123456", "-i", "123456"]
