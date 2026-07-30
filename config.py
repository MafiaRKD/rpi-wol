import json
from pathlib import Path

CONFIG_PATH = Path("config.json")


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            "config.json not found. Copy config.example.json to config.json."
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


CONFIG = load_config()