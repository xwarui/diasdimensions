#!/usr/bin/env python3
"""
centralize_nav.py

Does three things to every HTML file in your repo:
1. Removes the hardcoded <nav class="whispers">...</nav> block
2. Adds <script src="/components/nav-loader.js"></script> before </body>
3. Fixes the DOM paper abstract six/seven operator wording

Run from inside your repo folder:
    python3 centralize_nav.py

Backs up every changed file as filename.html.bak first.
To undo: python3 centralize_nav.py --restore
"""

import os
import re
import shutil
from pathlib import Path

REPO_DIR = Path(".")

NAV_SCRIPT_TAG = '  <script src="/components/nav-loader.js"></script>\n'

DOM_ABSTRACT_OLD = (
    'but as a sequence of seven  organizational operations'
)
DOM_ABSTRACT_NEW = (
    'but as a sequence of seven organizational operations'
)

DOM_SIX_OLD = (
    'a developmental sequence of irreducible organizational operators '
    '— Distinction, Relation, Action, Reception, Reflection, Organization —'
)
DOM_SIX_NEW = (
    'a developmental sequence of irreducible organizational operators '
    '— Distinction, Relation, Foundation, Action, Reception, Reflection, Organization — '
    'where Foundation serves as a stabilizing composite enabling structural coherence '
    'throughout the sequence —'
)

def find_html_files(root):
    files = []
    for p in Path(root).rglob("*.html"):
        if ".bak" in p.name:
            continue
        # skip the nav component itself
        if "components" in str(p):
            continue
        files.append(p)
    return files

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    html = original

    # ── 1. Remove hardcoded whispers nav ──
    # Matches <nav class="whispers"> ... </nav>
    html = re.sub(
        r'\n?<nav class="whispers">.*?</nav>\n?',
        '\n',
        html,
        flags=re.DOTALL
    )

    # ── 2. Add nav-loader script before </body> if not already there ──
    if 'nav-loader.js' not in html and '</body>' in html:
        html = html.replace('</body>', NAV_SCRIPT_TAG + '</body>')

    # ── 3. Fix DOM paper double-space typo in abstract ──
    html = html.replace(DOM_ABSTRACT_OLD, DOM_ABSTRACT_NEW)

    # ── 4. Fix six/seven operator wording in DOM paper abstract ──
    html = html.replace(DOM_SIX_OLD, DOM_SIX_NEW)

    if html != original:
        backup = str(path) + ".bak"
        shutil.copy(path, backup)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False

def main():
    files = find_html_files(REPO_DIR)
    print(f"Found {len(files)} HTML files\n")

    changed = []
    skipped = []

    for path in sorted(files):
        try:
            was_changed = fix_file(path)
            if was_changed:
                changed.append(path)
                print(f"  ✅ Updated: {path}")
            else:
                skipped.append(path)
                print(f"  ── No changes: {path}")
        except Exception as e:
            print(f"  ❌ Error on {path}: {e}")

    print(f"\n{'='*50}")
    print(f"Updated:   {len(changed)} files")
    print(f"Unchanged: {len(skipped)} files")
    print(f"\nBackups created as *.html.bak")
    print("Review, then delete .bak files when happy.")
    print("\nTo undo: python3 centralize_nav.py --restore")

def restore():
    count = 0
    for bak in Path(".").rglob("*.html.bak"):
        original = Path(str(bak).replace(".bak", ""))
        shutil.copy(bak, original)
        bak.unlink()
        count += 1
        print(f"  Restored: {original}")
    print(f"\nRestored {count} files")

if __name__ == "__main__":
    import sys
    if "--restore" in sys.argv:
        restore()
    else:
        main()
