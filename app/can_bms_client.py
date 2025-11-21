from __future__ import annotations
from abc import abstractmethod
from typing import List, Optional
import can
from pydantic import BaseModel


# ---------- Data models ----------
class BMSStatus(BaseModel):
    pack_voltage: float
    pack_current: float
    soc: float
    temp: List[float]
    contactor_closed: Optional[bool] = None


# ---------- Interface ----------


class BaseBMSClient(ABC):
    @abstractmethod
    def get_status(self) -> BMSStatus: ...

    @abstractmethod
    def get_alarms(self) -> list[str]: ...


# ---------- Fake implementation (for now) ----------


class FakeOrionBMSClient(BaseBMSClient):

    def get_status(self) -> BMSStatus:
        return BMSStatus(
            pack_voltage=400.0,
            pack_current=15.0,
            soc=75.0,
            temp=[25.0, 26.0, 27.5],
            contactor_closed=True,
        )

    def get_alarms(self) -> list[str]:
        return []


# ---------- Real CAN skeleton (to be filled later) ----------


class OrionCanBMSClient(BaseBMSClient):
    """
    Skeleton for talking to Orion BMS 2 over CAN.

    You’ll fill in:
      - correct bustype (socketcan, pcan, kvaser, etc.)
      - channel (e.g. 'can0', 'PCAN_USBBUS1', ...)
      - bitrate
      - CAN IDs / DBC decoding
    """

    def __init__(self, channel: str, bustype: str, bitrate: int):
        self.channel = channel
        self.bustype = bustype
        self.bitrate = bitrate
        self.bus = self._create_bus()

    def _create_bus(self) -> can.Bus:
        """
        Create a python-can Bus object.
        This will likely change depending on your hardware.
        """
        return can.interface.Bus(
            channel=self.channel,
            bustype=self.bustype,
            bitrate=self.bitrate,
        )

    def get_status(self) -> BMSStatus:
        """
        Minimal skeleton: read a few frames and parse them.

        When you know the Orion CAN frames, you will:
          - filter by specific arbitration IDs
          - extract bytes into voltage/current/SOC/temp
        """
        # TODO: replace this with real frame parsing
        # Example pattern (pseudo-code):
        #
        # msg = self.bus.recv(timeout=0.1)
        # if msg is None: handle timeout / keep last value
        #
        # if msg.arbitration_id == ORION_VOLTAGE_ID:
        #     voltage = parse_voltage(msg.data)
        # elif msg.arbitration_id == ORION_CURRENT_SOC_ID:
        #     ...
        #
        # For now just return placeholder:
        return BMSStatus(
            pack_voltage=0.0,
            pack_current=0.0,
            soc=0.0,
            temperatures=[],
            contactor_closed=None,
        )

    def get_alarms(self) -> list[str]:
        """
        Later: decode Orion fault/alarms frames from CAN.
        """
        # TODO: implement WHEN you have fault CAN IDs
        return []


# Choose which implementation the API uses:
# For now we use the fake one. When ready, swap to OrionCanBMSClient.

bms_client: BaseBMSClient = OrionCanBMSClient(
    channel="can0",
    bustype="socketcan",
    bitrate=500000,
)

bms_client: BaseBMSClient = FakeOrionBMSClient()
