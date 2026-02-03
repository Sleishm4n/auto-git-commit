import re
from collections import Counter

KEYWORDS = ["fix", "bug", "error", "test", "refactor", "cleanup"]

def parse(diff):
    files = re.findall(r"diff --git a/(.*?) b/", diff)

    added, removed = 0, 0

    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1

    text = diff.lower()
    found_keywords = [k for k in KEYWORDS if k in text]

    return {
        "files": files,
        "added": added,
        "removed": removed,
        "keywords": found_keywords
    }