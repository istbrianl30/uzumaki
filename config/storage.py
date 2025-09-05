import ast
from typing import List, Tuple
from pathlib import Path
from models import Card
from utils import get_cards_dir, safe_filename
import io

CARD_VAR = "CARD"

def _card_to_py(card: Card) -> str:
    # Escribe un archivo .py con un dict literal, 100% portable
    # Evita ejecutar nada al leer (solo eval literal del dict).
    content = io.StringIO()
    content.write("CARD = {\n")
    content.write(f'    "id": "{card.id}",\n')
    content.write(f'    "title": {repr(card.title)},\n')
    content.write(f'    "content": {repr(card.content)},\n')
    tags_list = "[" + ", ".join(repr(t) for t in card.tags) + "]"
    content.write(f'    "tags": {tags_list},\n')
    content.write(f'    "created": "{card.created}",\n')
    content.write(f'    "updated": "{card.updated}",\n')
    content.write("}\n")
    return content.getvalue()

def save_card(card: Card, target_dir: Path = None) -> Path:
    target_dir = target_dir or get_cards_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_filename(card.title, card.id)
    path = target_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(_card_to_py(card))
    return path

def update_card_file(path: Path, card: Card) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(_card_to_py(card))

def load_card_from_py(path: Path) -> Card:
    text = path.read_text(encoding="utf-8")
    # Parseo seguro: localiza la asignación CARD = { ... } y literal_eval
    module = ast.parse(text, filename=str(path))
    found = None
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == CARD_VAR:
                    if isinstance(node.value, (ast.Dict)):
                        found = ast.literal_eval(node.value)
    if not found or not isinstance(found, dict):
        raise ValueError(f"Archivo inválido: {path.name}")
    return Card(
        id=found.get("id", ""),
        title=found.get("title", ""),
        content=found.get("content", ""),
        tags=list(found.get("tags", [])),
        created=found.get("created", ""),
        updated=found.get("updated", ""),
    )

def load_all_cards(directory: Path = None) -> List[Tuple[Path, Card]]:
    directory = directory or get_cards_dir()
    directory.mkdir(parents=True, exist_ok=True)
    items: List[Tuple[Path, Card]] = []
    for path in sorted(directory.glob("*.py")):
        try:
            card = load_card_from_py(path)
            items.append((path, card))
        except Exception:
            # Ignora archivos inválidos (no rompe la app)
            continue
    return items
