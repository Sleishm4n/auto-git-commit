import subprocess

def get_diff():
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--cached"],
            stderr=subprocess.DEVNULL
        ).decode()

        if not diff.strip():
            diff = subprocess.check_output(
                ["git", "diff"],
                stderr=subprocess.DEVNULL
            ).decode()

        return diff
    except Exception:
        return ""