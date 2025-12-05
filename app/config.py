# app/config.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    MIN_SOC: float = 20.0
    MAX_SOC: float = 90.0
    MIN_PACK_VOLT: float = 320.0  # TODO: set to your real limits
    MAX_PACK_VOLT: float = 532.0
    MAX_TEMP_C: float = 40.0
    MAX_DISCHARGE_A: float = 250.0


LIMITS = Limits()


# CAN + Modbus placeholders (you’ll fill these later)
class CAN_IDS:
    STATUS_1 = 0x000  # TODO
    STATUS_2 = 0x000  # TODO


class MODBUS_REG:
    POWER_COMMAND = 1000  # TODO
    RESET_COMMAND = 1001  # TODO
    MASTER_ALARM = 1002  # TODO
