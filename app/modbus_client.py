# app/modbus_client.py
from app.config import MODBUS_REG


class PrincetonInverterClient:
    """
    High-level wrapper around Princeton inverter Modbus registers.
    Replace TODOs with real pymodbus calls.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 502):
        self.host = host
        self.port = port
        self.client = None  # real Modbus client goes here

    def connect(self) -> bool:
        # TODO: create pymodbus client and connect
        return True

    # ----- read commands / status -----
    def get_power_command(self) -> float:
        # TODO: read holding register MODBUS_REG.POWER_COMMAND
        return 0.0

    def get_reset_command(self) -> int:
        # TODO: read MODBUS_REG.RESET_COMMAND
        return 0

    def get_master_alarm(self) -> int:
        # TODO: read MODBUS_REG.MASTER_ALARM
        return 0

    # ----- write commands -----
    def set_power_command(self, value: float) -> None:
        # TODO: write holding register MODBUS_REG.POWER_COMMAND
        pass

    def inverter_on(self, on: bool) -> None:
        # e.g. power command 0 = off, >0 = on; or separate coil
        pass
