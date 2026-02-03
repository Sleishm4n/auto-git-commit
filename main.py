from diff import get_diff, has_changes
from parser import parse
from generator import generate_message
import subprocess

def main():
    diff = get_diff()

    if not has_changes():
        print("No changes detected.")
        return

    info = parse(diff)
    message = generate_message(info, diff)

    if isinstance(message, dict):
        subject = message['subject']
        body = message.get('body', '')
    else:
        subject = message
        body = ''

    print("\n" + "="*60)
    print("SUGGESTED COMMIT:")
    print("="*60)
    print(f"Subject: {subject}")
    print(f"\nDescription:\n{body}")
    print("="*60)
    print()

    choice = input("Proceed? [Y/n] ").strip().lower()

    if choice == "n":
        print("Cancelled.")
        return

    if body:
        subprocess.call(["git", "commit", "-m", subject, "-m", body])
    else:
        subprocess.call(["git", "commit", "-m", subject])
    print("\n Commit created successfully!")


if __name__ == "__main__":
    main()