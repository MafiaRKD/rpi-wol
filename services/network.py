import platform
import subprocess


def is_online(ip):
    """
    Returns True if host responds to a single ping.
    """

    param = "-n" if platform.system().lower() == "windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", param, "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return result.returncode == 0

    except Exception:
        return False