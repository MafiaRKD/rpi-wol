from flask import jsonify

from config import CONFIG
from services.network import is_online
from services.system import get_cpu_temp
from services.ups import get_ups_status


def get_status():
    """
    Returns current dashboard status as JSON.
    """

    devices = []

    for device in CONFIG["devices"]:
        devices.append(
            {
                "id": device["id"],
                "online": is_online(device["check_ip"]),
            }
        )

    return jsonify(
        {
            "cpu_temp": get_cpu_temp(),
            "devices": devices,
            "ups": get_ups_status(),
        }
    )