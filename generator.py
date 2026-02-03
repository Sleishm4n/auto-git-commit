import subprocess
from diff import get_diff, get_files

def llm_generate_full(diff):
    """Generate both commit message and description using LLM"""
    files = get_files()
    diff_content = get_diff()

    prompt = f"""You are analyzing a git diff. Generate a commit message based ONLY on what you see in the changes below.

Files changed:
{files}

Actual code changes:
{diff_content[:8000]}

Create a commit message in this EXACT format:
SUBJECT: [one line, max 50 chars, start with: Add/Fix/Update/Refactor/Remove]
BODY: [2-3 sentences describing ONLY what changed in the code above]

DO NOT invent features not shown in the diff. Only describe what you actually see.
"""
    
    try:
        proc = subprocess.Popen(
            ["ollama", "run", "qwen2.5:3b"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        
        out, _ = proc.communicate(prompt, timeout=45)
        
        if out:
            # Parse the output
            subject = None
            body = None
            
            lines = out.strip().split("\n")
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith("SUBJECT:"):
                    subject = line.replace("SUBJECT:", "").strip().strip('"').strip("'")
                elif line.startswith("BODY:"):
                    # Get the body (might be multiple lines)
                    body_lines = [line.replace("BODY:", "").strip()]
                    # Check if body continues on next lines
                    for next_line in lines[i+1:]:
                        next_line = next_line.strip()
                        if next_line and not next_line.startswith("SUBJECT") and not next_line.startswith("Example"):
                            body_lines.append(next_line)
                        else:
                            break
                    body = " ".join(body_lines).strip('"').strip("'")
            
            # Validate subject and body
            if subject and body and len(body) > 10:
                return {"subject": subject, "body": body}

    except Exception as e:
        print(f"LLM error: {e}")
        return None

def heuristic_generate_full(info):
    """Generate commit message and description using heuristics"""
    files = info["files"]
    added = info["added"]
    removed = info["removed"]
    keywords = info["keywords"]

    if not files:
        return {
            "subject": "Update project files",
            "body": "Makes general updates and improvements to project files."
        }

    # Get primary file
    target = files[0].split("/")[-1].split(".")[0] if files else "files"
    file_count = len(files)
    ext = files[0].split(".")[-1] if "." in files[0] else "file"
    
    # Determine action and description
    if "test" in keywords or any("test" in f for f in files):
        subject = f"Add tests for {target}"
        body = f"Adds {added} lines of test coverage for {target}. Includes test cases for core functionality."
    
    elif "fix" in keywords or "bug" in keywords:
        subject = f"Fix {target}"
        body = f"Resolves issues in {target}. Modified {added + removed} lines to address bugs and improve stability."
    
    elif removed > added * 2:
        subject = f"Refactor {target}"
        body = f"Refactors {target} to improve code quality. Removed {removed} lines of redundant code and simplified implementation."
    
    elif added > removed * 3:
        subject = f"Implement {target}"
        body = f"Adds new {target} functionality with {added} lines of code. Extends project capabilities with new features."
    
    elif file_count > 3:
        subject = f"Update {file_count} {ext} files"
        body = f"Updates {file_count} files with {added} additions and {removed} deletions. Improves overall codebase quality."
    
    else:
        subject = f"Update {target}"
        body = f"Updates {target} with {added} line additions and {removed} deletions. Modifies core functionality and improves implementation."
    
    return {"subject": subject, "body": body}

def generate_message(info, diff):
    """Generate full commit message with subject and body"""
    result = llm_generate_full(diff)
    
    if result and result.get('body'):
        print("LLM RAW:")
        print(f"  Subject: {result['subject']}")
        print(f"  Body: {result['body']}")
        return result
    else:
        print("LLM failed, using heuristics")
        return heuristic_generate_full(info)
