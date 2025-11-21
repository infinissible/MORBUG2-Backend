# main.py
from fastapi import FastAPI

# from .modbus_client import bms_client
from .can_bms_client import bms_client

app = FastAPI(title="EMS Backend", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/bms/status")
def get_bms_status():
    """
    High-level BMS status for the frontend / EMS logic.
    """
    return bms_client.get_status().model_dump()


@app.get("/bms/alarms")
def get_bms_alarms():
    return {"alarms": bms_client.get_alarms()}
