from diff import get_diff
from parser import parse
from generator import generate_message
import subprocess
import sys

def run():
    diff = get_diff()

    diff = diff[:3000]

    if not diff.strip():
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
    run()