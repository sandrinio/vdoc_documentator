import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import typer

class VDocConfig(BaseModel):
    api_key: Optional[str] = None
    project_id: Optional[str] = None

CONFIG_DIR_NAME = ".vdoc"
CONFIG_FILE_NAME = "config.json"

def get_config_path() -> Path:
    """Returns the path to the config file within the current working directory."""
    return Path.cwd() / CONFIG_DIR_NAME / CONFIG_FILE_NAME

def load_config() -> VDocConfig:
    """Loads the configuration from disk. Returns empty config if missing."""
    config_path = get_config_path()
    if not config_path.exists():
        return VDocConfig()
    
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
            return VDocConfig(**data)
    except (json.JSONDecodeError, OSError):
        return VDocConfig()

def save_config(config: VDocConfig) -> None:
    """Saves the configuration to disk, creating the directory if needed."""
    config_path = get_config_path()
    config_dir = config_path.parent
    
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        
    with open(config_path, "w") as f:
        # exclude_none=True to keep the file clean
        json.dump(config.model_dump(exclude_none=True), f, indent=2)

def ensure_vdoc_initialized():
    """Checks if .vdoc directory exists, raises error if not."""
    config_dir = Path.cwd() / CONFIG_DIR_NAME
    if not config_dir.exists():
        # strict check for certain commands
        pass 
