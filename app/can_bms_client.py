# app/can_bms_client.py
from dataclasses import dataclass


@dataclass
class BMSData:
    soc: float
    pack_voltage: float
    max_temp: float
    pack_current: float
    master_alarm: bool


class OrionBMSClient:
    """
    High-level wrapper around Orion BMS 2 CAN frames.
    Fill in CAN setup + parsing later.
    """

    def __init__(self, channel: str = "can0", bustype: str = "socketcan"):
        self.channel = channel
        self.bustype = bustype
        self.bus = None  # real python-can Bus goes here

    def connect(self) -> bool:
        # TODO: setup python-can Bus here
        # import can; self.bus = can.interface.Bus(...)
        return True

    def read_pack_data(self) -> BMSData:
        # TODO: read required frames, parse into BMSData
        # For now, return dummy values so EMS logic is testable.
        return BMSData(
            soc=50.0,
            pack_voltage=400.0,
            max_temp=25.0,
            pack_current=0.0,
            master_alarm=False,
        )
