import subprocess
from diff import get_diff, get_files

def phi_generate(diff):
    files = get_files()
    diff = get_diff()

    prompt = f"""Generate a git commit message and description for these changes.

Files: {files}

Changes:
{diff[:800]}

Format your response EXACTLY like this:
SUBJECT: <one line commit message, max 50 chars, imperative mood>
BODY: <2-3 sentences explaining what changed and why>

Example:
SUBJECT: Add user authentication system
BODY: Implements JWT-based authentication with login and registration endpoints. Includes password hashing using bcrypt and token refresh functionality. This provides secure user access control for the application.
"""
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
            subject, body = None, None

            lines = out.strip().split("\n")
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith("SUBJECT:"):
                    subject = line.replace("SUBJECT:", "").strip().strip()
                elif line.startswith("BODY:"):
                    body_lines = [line.replace("BODY:", "").strip()]
                    for next_line in lines[i+1:]:
                        if next_line.strip() and not next_line.startswith("SUBJECT"):
                            body_lines.append(next_line.strip())
                        else:
                            break
                    body = " ".join(body_lines).strip('"').strip("'")
            
            if subject and body:
                return {"subject": subject, "body": body}
            elif subject:
                return {"subject": subject, "body": f"Updates {files.split()[0] if files else 'project files'}."}


    except Exception as e:
        print(f"LLM error: {e}")
        return None

def heuristic_generate(info):
    files = info["files"]
    added = info["added"]
    removed = info["removed"]
    keywords = info["keywords"]

    if not files:
        return {
            "subject": "Update project files",
            "body": "General updates and improvements to project files."
        }

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

    if msg:
        print("LLM RAW:")
        print(f"  Subject: {msg['subject']}")
        print(f"  Body: {msg['body']}")
    else:
        print("LLM failed, using heuristics")
        msg = heuristic_generate(info)
    
    return msg
