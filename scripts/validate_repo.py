#!/usr/bin/env python3
"""Static structural checks for this library; not a behavioral evaluation."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
entries = sorted(root.glob("*/*/SKILL.md"))
failures = []
names = set()

if len(entries) < 13:
    failures.append("Expected at least 13 SKILL.md files")

for entry in entries:
    text = entry.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\nname:\s*([^\n]+)\ndescription:\s*([^\n]+)\n---", text)
    if not match:
        failures.append(f"{entry}: missing required frontmatter")
        continue
    name, desc = match.groups()
    if name != entry.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        failures.append(f"{entry}: invalid skill name")
    if name in names:
        failures.append(f"{entry}: duplicated name {name}")
    names.add(name)
    if not 1 <= len(desc.strip()) <= 1024:
        failures.append(f"{entry}: invalid description length")
    agent = entry.parent / "agents" / "openai.yaml"
    if not agent.exists():
        failures.append(f"{entry}: missing agents/openai.yaml")
        continue
    y = agent.read_text(encoding="utf-8")
    short = re.search(r'^  short_description: "([^"]+)"$', y, re.M)
    if not short or not 25 <= len(short.group(1)) <= 64:
        failures.append(f"{agent}: short_description must be 25-64 characters")
    if f"${name}" not in y or "default_prompt:" not in y:
        failures.append(f"{agent}: missing default_prompt mentioning skill name")

print(f"Skills analyzed: {len(entries)}; problems: {len(failures)}")
for failure in failures:
    print("ERROR:", failure)
sys.exit(bool(failures))
