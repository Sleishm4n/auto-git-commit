import subprocess
from diff import get_diff, get_files

def phi_generate(diff):
    files = get_files()
    diff = get_diff()

    prompt = f"""Generate a git commit message for these changes.

Files: {files}

Changes:
{diff[:600]}

Reply with ONLY the commit message (max 10 words, imperative mood).
Message:"""
    try:
        proc = subprocess.Popen(
            ["ollama", "run", "llama3.2:1b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        out, _ = proc.communicate(prompt, timeout=60)

        if out:
            lines = [line.strip() for line in out.strip().split("\n") if line.strip()]
            for line in lines:
                if len(line) > 5 and not line.startswith("To help") and not line.startswith("I "):
                    return line.strip('"').strip("'")
            if lines:
                return lines[0].strip('"').strip("'")

    except Exception as e:
        print(f"LLM error: {e}")
        return None

def heuristic_generate(info):
    files = info["files"]
    added = info["added"]
    removed = info["removed"]
    keywords = info["keywords"]

    if not files:
        return "Update project files"

    target = files[0].split("/")[-1].split(".")[0]

    if "test" in keywords:
        prefix = "Add tests for"
    elif "fix" in keywords or "bug" in keywords:
        prefix = "Fix"
    elif added > removed:
        prefix = "Implement"
    else:
        prefix = "Refactor"

    return f"{prefix} {target}"

def generate_message(info, diff):
    msg = phi_generate(diff)
    print("LLM RAW:", msg)

    if msg and len(msg) > 5:
        return msg
    
    return heuristic_generate(info)