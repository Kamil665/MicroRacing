import json
from pathlib import Path

SAVE_PATH = Path(__file__).parent / "data" / "save.json"

DEFAULT_SAVE = {
    "coins": 500,
    "best_time": None,
    "unlocked_cars": [0],
    "selected_car": 0,
    "selected_map": 0,
}

def load_save():
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SAVE_PATH.exists():
        save = DEFAULT_SAVE.copy()
        save_save(save)
        return save
    try:
        data = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        for key, value in DEFAULT_SAVE.items():
            data.setdefault(key, value)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SAVE.copy()

def save_save(data):
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SAVE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
