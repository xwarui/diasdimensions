import os
import re

# The pattern to find and remove
PRESENCE_PATTERN = re.compile(
    r'<!-- PRESENCE BAR -->[\s\S]*?<div class="presence">[\s\S]*?</div>\s*</div>\s*<a href="/publications/structural-ethical-orientation/" class="presence-action">Read the specification →</a>\s*</div>',
    re.IGNORECASE
)

# Alternative simpler pattern if the above doesn't match
SIMPLE_PATTERN = re.compile(r'<!-- PRESENCE BAR -->[\s\S]*?</div>\s*</div>\s*</div>', re.IGNORECASE)

def remove_presence_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Try the specific pattern first
    content = PRESENCE_PATTERN.sub('', content)
    
    # If nothing changed, try looking for any presence div
    if content == original:
        content = re.sub(
            r'<div class="presence">[\s\S]*?</div>\s*</div>\s*</div>',
            '',
            content
        )
        # Also remove the comment if it's still there
        content = re.sub(r'<!-- PRESENCE BAR -->', '', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Cleaned: {filepath}")
        return True
    return False

def main():
    cleaned = 0
    for root, dirs, files in os.walk('.'):
        # Skip hidden folders and common non-website folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if remove_presence_from_file(filepath):
                    cleaned += 1
    
    print(f"\n✓ Done! Cleaned {cleaned} files.")

if __name__ == "__main__":
    main()