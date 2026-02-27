#!/usr/bin/env python3
"""
centralize_nav.py

Does three things to every HTML file in your repo:
1. Removes the hardcoded <nav class="whispers">...</nav> block
2. Adds/fixes <script src="/components/nav-loader.js"></script> before </body>
3. Fixes any relative path versions of the script tag already injected
4. Fixes the DOM paper abstract six/seven operator wording

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

# The correct absolute script tag
NAV_SCRIPT_CORRECT = '  <script src="/components/nav-loader.js"></script>\n'

# All the relative path variants to find and fix
NAV_SCRIPT_VARIANTS = [
    '<script src="components/nav-loader.js"></script>',
    '<script src="../components/nav-loader.js"></script>',
    '<script src="../../components/nav-loader.js"></script>',
    '<script src="../../../components/nav-loader.js"></script>',
]

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
        if "components" in str(p):
            continue
        files.append(p)
    return files

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    html = original

    # 1. Remove hardcoded whispers nav
    html = re.sub(
        r'\n?<nav class="whispers">.*?</nav>\n?',
        '\n',
        html,
        flags=re.DOTALL
    )

    # 2. Fix any relative path script tags already in the file
    for variant in NAV_SCRIPT_VARIANTS:
        if variant in html:
            html = html.replace(variant, NAV_SCRIPT_CORRECT.strip())

    # 3. Add correct script tag if not present at all
    if '/components/nav-loader.js' not in html and '</body>' in html:
        html = html.replace('</body>', NAV_SCRIPT_CORRECT + '</body>')

    # 4. Fix DOM paper six/seven operator wording
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
                print(f"  FIXED: {path}")
            else:
                skipped.append(path)
                print(f"  -- No changes: {path}")
        except Exception as e:
            print(f"  ERROR on {path}: {e}")

    print(f"\n{'='*50}")
    print(f"Fixed:     {len(changed)} files")
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
