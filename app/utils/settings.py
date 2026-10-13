"""JSON persistence for user settings and recent calculations."""

import json
from datetime import datetime

from app.utils.paths import data_dir


DEFAULT_SETTINGS = {
    "version": 1,
    "theme": "dark",
    "mode": "standard",
    "angle_unit": "deg",
    "decimal_separator": ",",
    "always_on_top": False,
    "window": {"width": 400, "height": 640},
}


def _read_json(name: str, default):
    try:
        with (data_dir() / name).open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, ValueError, TypeError):
        return default


def _write_json(name: str, value) -> None:
    path = data_dir() / name
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
    temporary.replace(path)


def load_settings() -> dict:
    stored = _read_json("settings.json", {})
    settings = dict(DEFAULT_SETTINGS)
    settings.update(stored if isinstance(stored, dict) else {})
    settings["window"] = dict(DEFAULT_SETTINGS["window"], **settings.get("window", {}))
    return settings


def save_settings(settings: dict) -> None:
    _write_json("settings.json", settings)


def load_history() -> list:
    history = _read_json("history.json", [])
    return history[:100] if isinstance(history, list) else []


def append_history(history: list, expression: str, result: str) -> list:
    history.insert(0, {"expr": expression, "result": result, "time": datetime.now().isoformat(timespec="seconds")})
    history = history[:100]
    _write_json("history.json", history)
    return history


def clear_history() -> None:
    _write_json("history.json", [])