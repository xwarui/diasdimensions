import os
import re

def remove_presence_bar(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # The exact pattern to find and remove
    pattern = r'''<!-- PRESENCE BAR -->
<div class="presence">
  <div class="presence-mark"></div>
  <div class="presence-text">
    <strong>Current tension:</strong> The Pentagon demands Anthropic remove AI safety constraints\.
    External ethics can be stripped\. Internal orientation cannot\.
  </div>
  <a href="/publications/structural-ethical-orientation/" class="presence-action">Read the specification →</a>
</div>

  <script src="/components/nav-loader\.js"></script>
</body>
</html>'''
    
    # Replace with clean closing
    replacement = '''  <script src="/components/nav-loader.js"></script>
</body>
</html>'''
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Cleaned: {filepath}")
        return True
    else:
        # Try simpler version without the script line
        simple_pattern = r'''<!-- PRESENCE BAR -->
<div class="presence">
  <div class="presence-mark"></div>
  <div class="presence-text">
    <strong>Current tension:</strong> The Pentagon demands Anthropic remove AI safety constraints\.
    External ethics can be stripped\. Internal orientation cannot\.
  </div>
  <a href="/publications/structural-ethical-orientation/" class="presence-action">Read the specification →</a>
</div