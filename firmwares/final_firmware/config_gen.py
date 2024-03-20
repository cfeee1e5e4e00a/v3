from dataclasses import dataclass
import struct
import os

@dataclass
class Config:
    client_id: str
    room_ids: list[int]
    dht_pins: list[int]
    acs_pins: list[int]
    relay_pins: list[int]
    send_external_temp: bool
    external_dht_pin: int



config_1 = Config(
    "FLATCON1",
    room_ids=[1, 2],
    dht_pins=[25, 26],
    acs_pins=[34, 35],
    relay_pins=[21, 19, 18, 5],
    send_external_temp=False,
    external_dht_pin=99,
)

config_2 = Config(
    "FLATCON2",
    room_ids=[3, 4],
    dht_pins=[25, 26],
    acs_pins=[34, 35],
    relay_pins=[21, 19, 18, 5],
    send_external_temp=False,
    external_dht_pin=99,
)

config_3 = Config(
    "FLATCON3",
    room_ids=[5, 6],
    dht_pins=[25, 26],
    acs_pins=[34, 35],
    relay_pins=[21, 19, 18, 5],
    send_external_temp=False,
    external_dht_pin=99,
)

configs = [config_1, config_2, config_3]

def config_to_bytes(c: Config) -> bytes:
    ret = struct.pack('<16sbb', c.client_id.encode(), c.send_external_temp, c.external_dht_pin)
    for i in range(2):
        ret += struct.pack('<bbbbb', c.room_ids[i], c.dht_pins[i], c.acs_pins[i], *c.relay_pins[i*2:i*2+2])
    return ret


def upload_config(c: Config):
    data = config_to_bytes(c)
    fname = '/tmp/config_blob.bin'
    with open(fname, 'wb') as f:
        f.write(data)
    os.system(f'parttool.py write_partition --partition-name nticfg --input {fname}')


if __name__ == '__main__':
    import sys
    cn = int(sys.argv[1])  -1
    cfg = configs[cn]
    print(f'Config:', cfg)
    if input('Upload?')[0] != 'y':
        exit(0)
    print('Uploading')
    upload_config(cfg)