from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
version_file = root / ".dev-standard" / "VERSION"
override_file = root / ".dev-standard" / "PROJECT_OVERRIDES.md"
agents_file = root / "AGENTS.md"

errors = []
for path in [version_file, override_file, agents_file]:
    if not path.is_file():
        errors.append(f"missing: {path.relative_to(root)}")

if version_file.exists():
    value = version_file.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"ai-development-standard@v\d+\.\d+\.\d+", value):
        errors.append(f"invalid .dev-standard/VERSION: {value!r}")

if errors:
    print("project standard verification: FAIL")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print("project standard verification: PASS")
