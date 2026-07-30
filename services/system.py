from pathlib import Path


def get_cpu_temp():
    """
    Returns CPU temperature as a formatted string.
    On systems without a temperature sensor returns '-'.
    """

    thermal_zone = Path("/sys/class/thermal/thermal_zone0/temp")

    try:
        if thermal_zone.exists():
            temp = int(thermal_zone.read_text().strip()) / 1000
            return f"{temp:.1f}°C"
    except Exception:
        pass

    return "-"