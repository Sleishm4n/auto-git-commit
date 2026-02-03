import subprocess

def get_diff():
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--cached", "--", ".", ":(exclude)__pycache__", ":(exclude)*.pyc"],
            stderr=subprocess.DEVNULL
        ).decode()

        if not diff.strip():
            diff = subprocess.check_output(
                ["git", "diff", "--", ".", ":(exclude)__pycache__", ":(exclude)*.pyc"],
                stderr=subprocess.DEVNULL
            ).decode()

        if len(diff) > 800:
            diff = diff[-800:]

        return diff
    except Exception:
        return ""
    
def get_files():
    try:
        files = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--", ".", ":(exclude)__pycache__", ":(exclude)*.pyc"],
            text=True
        )
        return files.strip()
    
    except Exception:
        return ""
    
def has_changes():
    try:
        files = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--", ".", ":(exclude)__pycache__", ":(exclude)*.pyc"],
            text=True
        ).strip()
        return bool(files)
    
    except Exception:
        return False
