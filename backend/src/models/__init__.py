from .log_entry import LogEntry
from .user import User
from .bill import Bill
from .temp_schedule import TempScheduleEntry

type m2 = float
type m3 = float

P_max = 12  # max power of heater
α = 20  # air heat transfer coef for room
# TODO: Recalc using consts
dQ_to_V = 350.722  # heat per logarifmic ration of temperatures per volume
T_out = 24.2  # outside tempreture

_SIDE_WINDOWS_SIZE: m2 = 0.0093
_CENTRAL_WINDOWS_SIZE: m2 = 0.0057
_FLAT_WINDOWS_SIZE: dict[int, m2] = {
    1: _SIDE_WINDOWS_SIZE,
    2: _CENTRAL_WINDOWS_SIZE,
    3: _SIDE_WINDOWS_SIZE,
    4: _SIDE_WINDOWS_SIZE,
    5: _CENTRAL_WINDOWS_SIZE,
    6: _SIDE_WINDOWS_SIZE,
}

_SECOND_FLOOR_FLAT_VOLUME: m3 = 0.002
_FIRST_FLOOR_FLAT_VOLUME: m3 = 0.00225
_FLAT_VOLUME: dict[int, m3] = {
    1: _SECOND_FLOOR_FLAT_VOLUME,
    2: _SECOND_FLOOR_FLAT_VOLUME,
    3: _SECOND_FLOOR_FLAT_VOLUME,
    4: _FIRST_FLOOR_FLAT_VOLUME,
    5: _FIRST_FLOOR_FLAT_VOLUME,
    6: _FIRST_FLOOR_FLAT_VOLUME,
}
