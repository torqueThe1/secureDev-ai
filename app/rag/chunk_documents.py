
def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Invalid chunk size or overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            search_start = start + chunk_size // 2

            # Prefer splitting at paragraph boundaries
            split_at = text.rfind("\n\n", search_start, end)

            # Otherwise, split at a word boundary
            if split_at != -1:
                end = split_at + 2
            else:
                split_at = text.rfind(" ", search_start, end)
                if split_at != -1:
                    end = split_at + 1

        chunks.append(text[start:end].strip())

        if end == len(text):
            break

        start = end - overlap

        # Avoid starting in the middle of a word
        while start < len(text) and start > 0 and not text[start - 1].isspace():
            start += 1

    return chunks
