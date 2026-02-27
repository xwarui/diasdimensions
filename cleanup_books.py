#!/usr/bin/env python3
"""
cleanup_books.py
Fixes formatting issues across all diasdimensions.org HTML files.

What it fixes:
- Removes double-wrapped room-body / content-body divs
- Removes old .book-nav elements (duplicate of seq-nav)
- Removes stray ### and ## markdown artifacts
- Fixes <p> tags inside <li> items
- Removes .book-movement and .book-operator orphan paragraphs styling
- Cleans up the h1 inside content (page already has h1 in page-header)

Run from inside your repo folder:
    python3 cleanup_books.py

It will back up every file it touches as filename.html.bak before changing anything.
"""

import os
import re
import shutil
from pathlib import Path

# ── Find all HTML files in the repo ──
REPO_DIR = Path(".")  # run from inside your repo folder

def find_html_files(root):
    files = []
    for p in Path(root).rglob("*.html"):
        # skip backups
        if ".bak" in p.name:
            continue
        files.append(p)
    return files

def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    html = original

    # ── 1. Remove stray markdown headings (### and ##) sitting as bare text ──
    # Matches lines that are just ### or ## optionally with spaces
    html = re.sub(r'^\s*#{2,3}\s*$', '', html, flags=re.MULTILINE)

    # ── 2. Remove <p class="book-movement">...</p> ──
    html = re.sub(r'<p class="book-movement">.*?</p>', '', html, flags=re.DOTALL)

    # ── 3. Remove <p class="book-operator">...</p> ──
    html = re.sub(r'<p class="book-operator">.*?</p>', '', html, flags=re.DOTALL)

    # ── 4. Remove old <nav class="book-nav">...</nav> ──
    html = re.sub(r'<nav class="book-nav">.*?</nav>', '', html, flags=re.DOTALL)

    # ── 5. Fix <p> tags inside <li> items ──
    # Pattern: <li>...<p>content</p>...</li> → <li>...content...</li>
    # Remove opening <p> inside <li>
    html = re.sub(r'(<li[^>]*>)\s*<p>', r'\1', html)
    # Remove closing </p> before </li>
    html = re.sub(r'</p>\s*(</li>)', r'\1', html)
    # Remove orphan <p> tags that appear between </li> and <li> (stray paragraph continuations)
    html = re.sub(r'</li>\s*<p>(.*?)</p>\s*(<li|</ul>)', 
                  lambda m: f'</li>\n{m.group(2)}', html, flags=re.DOTALL)

    # ── 6. Unwrap double room-body / content-body nesting ──
    # The pattern is:
    # <article class="room-body">
    #   <div class="room-body">
    #     <article class="content-body">
    #       ... actual content ...
    #     </article>
    #   </div>
    # </article>
    # We want just the actual content inside, no wrappers

    # Remove inner <div class="room-body"> opening tag
    html = re.sub(r'(<article class="room-body">\s*)\n\s*<div class="room-body">', 
                  r'\1', html)
    # Remove inner <article class="content-body"> opening tag  
    html = re.sub(r'<article class="content-body">', '', html)
    # Remove the closing </article> and </div> that belonged to the inner wrappers
    # This is trickier — we look for the pattern of double-close before seq-nav or end of main
    html = re.sub(r'</article>\s*\n\s*</div>\s*\n(\s*</article>)', r'\n\1', html)

    # ── 7. Remove duplicate h1 inside content body ──
    # The page-header already has the h1, so the one inside the article is redundant
    # Only remove if there's already a page-title h1 in the file
    if 'class="page-title"' in html:
        # Remove the first <h1>...</h1> inside the article content area
        # Be careful not to remove the page-title one
        html = re.sub(r'(<article class="room-body">.*?)<h1>.*?</h1>', 
                      r'\1', html, count=1, flags=re.DOTALL)

    # ── 8. Clean up excess blank lines (more than 2 in a row) ──
    html = re.sub(r'\n{3,}', '\n\n', html)

    # ── Only write if something changed ──
    if html != original:
        # Back up original
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
                print(f"  ✅ Fixed: {path}")
            else:
                skipped.append(path)
                print(f"  ── No changes: {path}")
        except Exception as e:
            print(f"  ❌ Error on {path}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Fixed:     {len(changed)} files")
    print(f"Unchanged: {len(skipped)} files")
    print(f"\nBackup files created as *.html.bak")
    print("Review changes, then delete .bak files when happy.")
    print("\nTo undo ALL changes, run:")
    print("  python3 cleanup_books.py --restore")

def restore():
    """Restore all .bak files"""
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
