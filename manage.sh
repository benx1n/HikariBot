#!/bin/bash

ENV_CONFIG_NAME=".env.prod"

if [ $# -eq 0 ]
then
	echo "Usage: ./manage.sh [VERB] [OPTION...]"
	echo "Verb: "
	echo "  Install"
	echo "  Start"
	echo "  Update"
	echo "Option: "
	echo "  -t, --token  Followed by token"
	echo "  -i, --id     Followed by ID of QQ"
elif [ $1 = "install" ]
then
	echo "Installing dependences."
	sudo apt-get update
	if [ $? -ne 0 ]
	then 
		yum update
	fi
	sudo apt-get install -y locales locales-all fonts-noto libnss3-dev libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1
	if [ $? -ne 0 ]
	then 
		yum install -y at-spi2-atk-2.26.2-1.el7.x86_64 libXcomposite-0.4.4-4.1.el7.x86_64 libXdamage-1.1.4-4.1.el7.x86_64 libXrandr-1.5.1-2.el7.x86_64 mesa-libgbm-18.3.4-12.el7_9.x86_64 libxkbcommon-0.7.1-3.el7.x86_64 pango-1.42.4-4.el7_7.x86_64 cairo-1.15.12-4.el7.x86_64
	fi
	echo "Installing HikariBot"
	pip install nb-cli hikari-bot nonebot-plugin-gocqhttp
	playwright install chromium
elif [ $1 = "start" ]
then
	if [ -e ${ENV_CONFIG_NAME} ]
	then
		echo "OK"
		nb run
	else
		ENV_CONFIG_EXAMPLE=`cat ${ENV_CONFIG_NAME}-example`
		TOKEN=
		QQ_ID=
		NEXT_TOKEN=false
		NEXT_QQ_ID=false
		for name in $*
		do
			if [ ${NEXT_TOKEN} = ture ]
			then
				TOKEN=${name}
				NEXT_TOKEN=false
			elif [ ${NEXT_QQ_ID} = ture ]
			then
				QQ_ID=${name}
				NEXT_QQ_ID=false
			elif [[ ${name} = "-t" || ${name} = "--token" ]]
			then
				NEXT_TOKEN=ture
			elif [[ ${name} = "-i" || ${name} = "--id" ]]
			then
				NEXT_QQ_ID=ture
			fi
		done
		if [[ -z ${TOKEN} || -z ${QQ_ID} ]]
		then
			echo "Token and id of QQ must be given."
			exit
		fi
		ENV_CONFIG_EXAMPLE=${ENV_CONFIG_EXAMPLE/'123456:qwertyuiopasdfghjl'/${TOKEN}}
		ENV_CONFIG_EXAMPLE=${ENV_CONFIG_EXAMPLE/'1119809439'/${QQ_ID}}
		echo "${ENV_CONFIG_EXAMPLE}" > ${ENV_CONFIG_NAME}
		nb run
	fi
elif [ $1 = "update" ]
then
	pip install --upgrade hikari-bot
	git pull
else
	echo "Unrecognized verb $1."
fi
