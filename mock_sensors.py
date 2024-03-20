mqtt_addr = 'mqtt.cfeee1e5e4e00a.ru'

import paho.mqtt.client as mqtt
import random
from math import sin




client = mqtt.Client('mock')
client.username_pw_set("nti", "nti")
client.connect(mqtt_addr)


from time import sleep, time

client.loop_start()

client.publish("/init", f'power,esp=mock value=1')

delay = 0.5
i = 0
rw_step = 0.6

def pub(m: str, room: int, value: float):
    client.publish("/sensors", f'{m},flat={room} value={float(value)}')

values = [0] * 6

try: 
    while True:
        for room in range(6):
            vmin = (room + 1) * 10
            vmax = vmin + 9
            values[room] = values[room] + rw_step * random.choice([1, -1])
            values[room] = min(max(values[room], vmin), vmax)
            pub('temp', room+1, values[room])

            pub("humd", room+1, sin(time()/20)*5+((room+1)*10 + 5))

            pub("curr", room+1, i - int(i)//10*10 + (room+1)*10)


        i += 0.1
        sleep(delay)
except KeyboardInterrupt:
    pass


client.loop_stop()