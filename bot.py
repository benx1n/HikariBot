#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter
from nonebot.log import default_format, logger

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
config = nonebot.get_driver().config
config.nb2_path = Path(__file__).parent


if __name__ == "__mp_main__" or ("run" in sys.argv and "nb" in sys.argv[0]):
    logger.add(
        "logs/error.log",
        rotation="00:00",
        retention="1 week",
        diagnose=False,
        level="ERROR",
        format=default_format,
        encoding="utf-8",
    )
    logger.add(
        "logs/info.log",
        rotation="00:00",
        retention="1 week",
        diagnose=False,
        level="INFO",
        format=default_format,
        encoding="utf-8",
    )
    logger.add(
        "logs/warning.log",
        rotation="00:00",
        retention="1 week",
        diagnose=False,
        level="WARNING",
        format=default_format,
        encoding="utf-8",
    )
    if driver.config.use_plugin_go_cqhttp:
        nonebot.load_plugin("nonebot_plugin_gocqhttp")
    nonebot.load_from_toml("pyproject.toml")
    # ...

if __name__ == "__main__":
    # logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.load_plugin("nonebot_plugin_reboot")
    nonebot.run(app="__mp_main__:app")
