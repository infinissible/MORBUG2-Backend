from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel


class BMSStatus(BaseModel):
    pack_voltage: float
    pack_current: float
    soc: float
    temp: List[float]


class BaseBMSClient(ABC):
    """Interface that any BMS implementation must follow."""

    @abstractmethod
    def get_status(self) -> BMSStatus: ...

    @abstractmethod
    def get_alarms(self) -> list[str]: ...


class FakeOrionBMSClient(BaseBMSClient):
    """
    Fake client used during early development.
    Replace later with a real OrionBMSClient that talks over CAN/IP.
    """

    def get_status(self) -> BMSStatus:
        return BMSStatus(
            pack_voltage=400.0,
            pack_current=10.0,
            soc=80.0,
            temperatures=[25.0, 26.5, 27.0],
        )

    def get_alarms(self) -> list[str]:
        return []  # no alarms in fake mode
