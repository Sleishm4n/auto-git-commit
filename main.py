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

    print("Suggested commit:")
    print(message)
    print()

    choice = input("Proceed? [Y/n] ").strip().lower()

    if choice == "n":
        print("Cancelled.")
        return

    subprocess.call(["git", "commit", "-m", message])

if __name__ == "__main__":
    main()