# app/main.py
from enum import Enum, auto
from time import sleep

from app.can_bms_client import OrionBMSClient
from app.modbus_client import PrincetonInverterClient
from app.config import LIMITS


class EMSState(Enum):
    INIT = auto()
    PRECHECK = auto()
    IDLE = auto()
    RUNNING = auto()
    END = auto()
    FAULT = auto()


class EMS:
    def __init__(self):
        self.state = EMSState.INIT
        self.bms = OrionBMSClient()
        self.inv = PrincetonInverterClient()
        self.last_fault: str | None = None

    # ------------- main step -------------
    def step(self):
        if self.state is EMSState.INIT:
            self._init_state()
        elif self.state is EMSState.PRECHECK:
            self._precheck()
        elif self.state is EMSState.IDLE:
            self._idle()
        elif self.state is EMSState.RUNNING:
            self._running()
        elif self.state is EMSState.END:
            self._end_cycle()
        elif self.state is EMSState.FAULT:
            self._fault_state()

    # ------------- states -------------
    def _init_state(self):
        if not (self.bms.connect() and self.inv.connect()):
            return self._fault("CONNECT_FAIL")

        # Inverter on command
        self.inv.inverter_on(True)

        data = self.bms.read_pack_data()
        if data.master_alarm:
            return self._fault("MASTER_ALARM")

        self.state = EMSState.IDLE

    def _precheck(self):
        data = self.bms.read_pack_data()

        if not (LIMITS.MIN_SOC <= data.soc <= LIMITS.MAX_SOC):
            return self._fault("SOC_RANGE")

        if not (LIMITS.MIN_PACK_VOLT <= data.pack_voltage <= LIMITS.MAX_PACK_VOLT):
            return self._fault("VOLT_RANGE")

        if data.max_temp > LIMITS.MAX_TEMP_C:
            return self._fault("TEMP_HIGH")

        self.state = EMSState.RUNNING

    def _idle(self):
        """System idle/standby – wait for non-zero power command."""
        power_cmd = self.inv.get_power_command()
        if power_cmd == 0:
            return
        self.state = EMSState.PRECHECK  # go through safety checks first

    def _running(self):
        data = self.bms.read_pack_data()
        power_cmd = self.inv.get_power_command()

        if power_cmd == 0:
            self.state = EMSState.END
            return

        # Flowchart safety checks
        if not (LIMITS.MIN_SOC <= data.soc <= LIMITS.MAX_SOC):
            return self._fault("SOC_LIMIT")
        if not (LIMITS.MIN_PACK_VOLT <= data.pack_voltage <= LIMITS.MAX_PACK_VOLT):
            return self._fault("VOLT_LIMIT")
        if data.max_temp > LIMITS.MAX_TEMP_C:
            return self._fault("TEMP_LIMIT")
        if abs(data.pack_current) > LIMITS.MAX_DISCHARGE_A:
            return self._fault("CURRENT_LIMIT")

        # All good – apply power command
        self.inv.set_power_command(power_cmd)

    def _end_cycle(self):
        """Charge / discharge end – verify pack OK then go idle."""
        data = self.bms.read_pack_data()
        if data.master_alarm:
            return self._fault("END_MASTER_ALARM")

        self.inv.set_power_command(0)
        self.state = EMSState.IDLE

    def _fault_state(self):
        self.inv.inverter_on(False)
        self.inv.set_power_command(0)

        reset = self.inv.get_reset_command()
        if reset == 1:
            self.last_fault = None
            self.state = EMSState.INIT

    # ------------- helpers -------------
    def _fault(self, code: str):
        self.last_fault = code
        print(f"[FAULT] {code}")
        self.state = EMSState.FAULT


def main():
    ems = EMS()
    while True:
        ems.step()
        sleep(0.1)  # 100 ms loop – adjust to your needs


if __name__ == "__main__":
    main()
