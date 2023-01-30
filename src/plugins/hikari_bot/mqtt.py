import asyncio
import gzip
import io
import json
from threading import Thread

import paho.mqtt.client as mqtt
from loguru import logger

from .wws_realTime import send_realTime_message


def on_connect(client, userdata, flag, rc):
    if rc == 0:  # 连接成功
        print("Connection successful")
    elif rc == 1:  # 协议版本错误
        print("Protocol version error")
    elif rc == 2:  # 无效的客户端标识
        print("Invalid client identity")
    elif rc == 3:  # 服务器无法使用
        print("server unavailable")
    elif rc == 4:  # 错误的用户名或密码
        print("Wrong user name or password")
    elif rc == 5:  # 未经授权
        print("unaccredited")
    print("Connect with the result code " + str(rc))


def on_disconnect(client, userdata, rc):
    #  rc == 0回调被调用以响应disconnect（）调用
    # 如果以任何其他值断开连接是意外的，例如可能出现网络错误。
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


# 当收到关于客户订阅的主题的消息时调用。
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    compressedstream = io.BytesIO(msg.payload)
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    data = gzipper.read()
    logger.success("==================接收到订阅===================")
    json_msg = json.loads(data)
    logger.success(json_msg)
    asyncio.run(select_mqtt_fuction(json_msg))
    pass


# 当使用使用publish()发送的消息已经传输到代理时被调用。
def on_publish(client, obj, mid):
    print("on_Publish, mid: " + str(mid))


# 当代理响应订阅请求时被调用
def on_subscribe(client, userdata, mid, granted_qos):
    print("on_Subscribed: " + str(mid) + " " + str(granted_qos))


# 当代理响应取消订阅请求时调用。
def on_unsubscribe(client, userdata, mid):
    print("on_unsubscribe, mid: " + str(mid))


# 当客户端有日志信息时调用
def on_log(client, obj, level, string):
    logger.success("on_Log:" + string)


def mqtt_subscribe():
    global client
    client.loop_forever()


# client = mqtt.Client(f"yuyuko_Hikari_{bot_info['user_id']}")


def mqtt_run(qq_id):
    # 账号密码验证放到最前面
    global client
    client = mqtt.Client(f"yuyuko_Hikari_{qq_id}")
    client.username_pw_set("wows-poll", "wows-poll")
    # client = mqtt.Client()
    # 建立mqtt连接
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    # 当与代理断开连接时调用
    client.on_disconnect = on_disconnect

    client.on_log = on_log

    # 绑定 MQTT 服务器地址
    broker_ip = "mq.wows.shinoaki.com"
    # MQTT服务器的端口号
    # client.connect(host=broker_ip, port=1883, keepalive=6000)
    client.connect(host=broker_ip, port=1883, keepalive=60)
    client.reconnect_delay_set(min_delay=1, max_delay=2000)
    client.subscribe(f"wows/bot/poll/real/{qq_id}", qos=2)

    # 创建线程去持续接收订阅信息
    subscribe_thread = Thread(target=mqtt_subscribe)
    subscribe_thread.start()


async def select_mqtt_fuction(data):
    await send_realTime_message(data)


# mqtt_run()
