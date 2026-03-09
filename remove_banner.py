import os

def remove_presence_bar(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # The exact text to find
    old_text = """<!-- PRESENCE BAR -->
<div class="presence">
  <div class="presence-mark"></div>
  <div class="presence-text">
    <strong>Current tension:</strong> The Pentagon demands Anthropic remove AI safety constraints.
    External ethics can be stripped. Internal orientation cannot.
  </div>
  <a href="/publications/structural-ethical-orientation/" class="presence-action">Read the specification →</a>
</div>"""
    
    # Replace with nothing
    new_content = content.replace(old_text, "")
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Cleaned: " + filepath)
        return True
    return False

def main():
    cleaned = 0
    for root, dirs, files in os.walk('.'):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if remove_presence_bar(filepath):
                    cleaned += 1
    
    print("Done! Cleaned " + str(cleaned) + " files.")

if __name__ == "__main__":
    main()