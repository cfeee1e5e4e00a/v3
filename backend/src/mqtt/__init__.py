import asyncio
from contextlib import asynccontextmanager

from gmqtt import Client as MQTTClient

MQTT_HOST = 'mqtt'


client = MQTTClient('py_back')


lat_val = ''
def get_last_val():
    return lat_val

def on_message(client, topic, payload: bytes, qos, properties):
    global lat_val
    print(f'Got message: {topic}: {payload}', flush=True)
    lat_val = payload
    mqtt_publish("/act/led/0", str(int(int(payload.decode().split('=')[-1])/4096*255)))


def mqtt_publish(topic: str, payload: str):
    client.publish(topic, payload)



async def init_mqtt():
    async def connect():
        client.set_auth_credentials('nti', 'nti')
        await client.connect(MQTT_HOST)

    def reconnect(client, packet, exc=None):
        print('MQTT disconnected, reconnecting')
        asyncio.get_running_loop().create_task(client.connect(MQTT_HOST))

    def on_connected(client, flags, rc, properties):
        client.subscribe("/sensors/#")

    client.on_connect = on_connected
    client.on_disconnect = reconnect
    client.on_message = on_message

    await connect()
