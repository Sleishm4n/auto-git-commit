import subprocess

def phi_generate(diff):
    prompt = f"""
Generate a consice git commit message (max 12 words) describing these changes:
{diff}
"""
    try:
        proc = subprocess.Popen(
            [r"C:/Users/samgl/AppData/Local/Programs/Ollama/ollama.exe", "run", "phi"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        out, _ = proc.communicate(prompt, timeout=60)

        if out:
            return out.strip().split("\n")[0]

    except Exception:
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