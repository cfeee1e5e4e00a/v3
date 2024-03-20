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
    "First",
    room_ids=[1, 2],
    dht_pins=[27, 26],
    acs_pins=[35, 34],
    relay_pins=[5, 18, 19, 21],
    send_external_temp=False,
    external_dht_pin=99,
)


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
    upload_config(config_1)