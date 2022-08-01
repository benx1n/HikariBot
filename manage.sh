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
	sudo apt-get install -y locales locales-all fonts-noto libnss3-dev libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1
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
