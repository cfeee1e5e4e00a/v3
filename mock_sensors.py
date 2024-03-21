mqtt_addr = 'mqtt.cfeee1e5e4e00a.ru'

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
import random
from math import sin




client = mqtt.Client('mock')
client.username_pw_set("nti", "nti")
@client.connect_callback()
def on_connect(client, userdata, flags, reasonCode):
    print('Connected to mqtt')
    client.subscribe("/mode/#")
    for i in range(1, 7):
        client.publish(f'/startup/{i}', 'fuck')
    print('sent startup notifications')

@client.message_callback()
def on_message_callback(client, userdata, message: MQTTMessage):
    room = int(message.topic.split('/')[-1]) - 1
    args = message.payload.decode().split(' ')
    mode = int(args[0])
    modes[room] = mode
    print(f'Set mode for room {room + 1}: {mode}')
    if mode == 3:
        # Off
        setpoints[room] = 0
    elif mode in [0, 1]:
        # constant
        setpoints[room] = float(args[1])
    elif mode == 2:
        trend_start_temps[room] = trend_target_temps[room]
        trend_target_temps[room] = float(args[1])
        trend_start_times[room] = time()
        trend_target_times[room] = time() + int(args[2])

client.connect(mqtt_addr)


from time import sleep, time

client.loop_start()

# simulation
modes = [0] * 6
setpoints = [0] * 6
trend_target_temps = [0] * 6
trend_target_times = [0] * 6
trend_start_times = [0] * 6
trend_start_temps = [0] * 6


# client.publish("/init", f'power,esp=mock value=1')

delay = 5
i = 0
rw_step = 0.6

def pub(m: str, room: int, value: float):
    client.publish("/sensors", f'{m},flat={room} value={float(value)}')

values = [0] * 6

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


try: 
    while True:
        for room in range(6):
            if modes[room] == 2:  # trend
                setpoints[room] = map_range(min(time(), trend_target_times[room]), trend_start_times[room], trend_target_times[room], trend_start_temps[room], trend_target_temps[room])
            vmin = (room + 1) * 10
            vmax = vmin + 9
            values[room] = values[room] + rw_step * random.choice([1, -1])
            values[room] = min(max(values[room], vmin), vmax)
            pub('temp', room+1, values[room])
            pub("humd", room+1, sin(time()/20)*5+((room+1)*10 + 5))
            pub("curr", room+1, i - int(i)//10*10 + (room+1)*10)

            pub("mode", room+1, modes[room])
            pub("set_temp", room+1, setpoints[room])

        print(f'Sent data {i}')
        i += 0.1
        sleep(delay)
except KeyboardInterrupt:
    pass


client.loop_stop()