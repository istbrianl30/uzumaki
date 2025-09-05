import uuid
from pathlib import Path
import platform
import re

APP_FOLDER_NAME = "UzumakiCards"

def generate_id() -> str:
    return str(uuid.uuid4())

def get_cards_dir() -> Path:
    # Documents del usuario en Windows; en otros SO usa home/Documents
    home = Path.home()
    docs = Path.home() / "Documents"
    base = docs if docs.exists() else home
    path = base / APP_FOLDER_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "card"

def safe_filename(title: str, uid: str) -> str:
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{ts}_{slugify(title)}_{uid[:8]}.py"
