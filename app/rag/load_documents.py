
from pathlib import Path

data_dir = Path("data/raw")

for file_path in data_dir.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    print(f"{file_path.name}: {len(text)} characters")
