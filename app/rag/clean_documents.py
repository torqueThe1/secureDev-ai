
import re


def clean_markdown(text: str) -> str:
    # Remove heading anchor IDs
    text = re.sub(r"\s*\{\s*#[\w-]+\s*\}", "", text)

    # Convert HTML abbreviations to readable text
    text = re.sub(
        r'<abbr title="([^"]+)">([^<]+)</abbr>',
        r'\2 (\1)',
        text
    )

    return text
