from diff import get_diff, get_files, has_changes
from parser import parse

print("=== DEBUGGING ===")
print(f"Has changes: {has_changes()}")
print(f"\nFiles detected:")
files = get_files()
print(files if files else "(none)")

print(f"\nDiff preview:")
diff = get_diff()
print(diff[:500] if diff else "(none)")

print(f"\nParsed info:")
info = parse(diff)
print(f"  Files: {info['files']}")
print(f"  Added: {info['added']}")
print(f"  Removed: {info['removed']}")
print(f"  Keywords: {info['keywords']}")