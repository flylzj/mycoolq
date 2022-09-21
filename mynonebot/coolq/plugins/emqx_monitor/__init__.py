# coding: utf-8
import nonebot


export = nonebot.require("nonebot_plugin_mqtt")


def on_message(client, topic, payload, qos, properties):
    print(client)
    print(topic)


export.mqtt_client.on_message = on_message