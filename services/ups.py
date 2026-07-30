import subprocess

from config import CONFIG


def get_ups_status():
    """
    Returns UPS status from NUT server.

    Returns None when UPS monitoring is disabled or unavailable.
    """

    if not CONFIG["ups"]["enabled"]:
        return None

    host = CONFIG["ups"]["host"]
    name = CONFIG["ups"]["name"]

    try:
        output = subprocess.check_output(
            [
                "upsc",
                f"{name}@{host}",
            ],
            text=True,
            timeout=3,
        )

    except FileNotFoundError:
        return None

    except Exception as e:
        print(f"UPS unavailable: {e}")
        return None

    values = {}

    for line in output.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()

    return {
        "status": values.get("ups.status"),
        "battery": values.get("battery.charge"),
        "runtime": values.get("battery.runtime"),
        "load": values.get("ups.load"),
        "input_voltage": values.get("input.voltage"),
        "output_voltage": values.get("output.voltage"),
    }