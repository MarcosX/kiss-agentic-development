import re
from pathlib import Path


def build_index(content_dir):
    index = {}
    for path in Path(content_dir).glob("*.md"):
        text = path.read_text()
        for term in re.split(r"[^a-zA-Z0-9]+", text.lower()):
            if term:
                index.setdefault(term, []).append(str(path))
    return index
