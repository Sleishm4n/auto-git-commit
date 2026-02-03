import re
from diff import get_files

KEYWORDS = ["fix", "bug", "error", "test", "refactor", "cleanup"]

def parse(diff):
    files_str = get_files()
    files = files_str.split('\n') if files_str else []
    files = [f.strip() for f in files if f.strip()]
    
    diff_files = re.findall(r"diff --git a/(.*?) b/", diff)
    if diff_files and not files:
        files = diff_files

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