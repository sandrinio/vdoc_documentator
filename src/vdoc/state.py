import json
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel

class VDocState(BaseModel):
    last_run: Optional[str] = None
    # flexible dictionary to store other state items
    local_context: Dict[str, Any] = {}

STATE_FILE_NAME = "state.json"
CONFIG_DIR_NAME = ".vdoc"

def get_state_path() -> Path:
    return Path.cwd() / CONFIG_DIR_NAME / STATE_FILE_NAME

def load_state() -> VDocState:
    state_path = get_state_path()
    if not state_path.exists():
        return VDocState()
    
    try:
        with open(state_path, "r") as f:
            data = json.load(f)
            return VDocState(**data)
    except Exception:
        return VDocState()

def save_state(state: VDocState) -> None:
    state_path = get_state_path()
    # Assume directory exists as config usually takes care of it, 
    # but good measure to ensure parent exists
    state_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(state_path, "w") as f:
        json.dump(state.model_dump(), f, indent=2)
