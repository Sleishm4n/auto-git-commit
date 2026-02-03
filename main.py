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

    print("\n" + "="*60)
    print("SUGGESTED COMMIT:")
    print("="*60)
    print(f"Subject: {message['subject']}")
    print(f"\nDescription:\n{message['body']}")
    print("="*60)
    print()

    choice = input("Proceed? [Y/n] ").strip().lower()

    if choice == "n":
        print("Cancelled.")
        return

    subprocess.call(["git", "commit", "-m", message['subject'], "-m", message['body']])
    print("\n Commit created successfully!")


if __name__ == "__main__":
    main()