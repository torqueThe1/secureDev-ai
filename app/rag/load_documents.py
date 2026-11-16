
from pathlib import Path
from app.rag.clean_documents import clean_markdown

raw_dir = Path("data/raw")
processed_dir = Path("data/processed")

processed_dir.mkdir(parents=True, exist_ok=True)

for file_path in raw_dir.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")
    cleaned_text = clean_markdown(text)

    output_path = processed_dir / file_path.name
    output_path.write_text(cleaned_text, encoding="utf-8")

    print(f"Processed: {file_path.name}")
