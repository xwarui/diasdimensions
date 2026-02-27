/* ============================================================
   nav-loader.js
   Fetches /components/nav.html and injects it into the page.
   Handles active state detection automatically.
   ============================================================ */

(function() {
  // Find the depth of current page to build correct path to components
  const path = window.location.pathname;
  const depth = (path.match(/\//g) || []).length - 1;
  const prefix = depth <= 1 ? '' : '../'.repeat(depth - 1);

  // Remove any hardcoded nav that was in the HTML
  const existing = document.getElementById('site-nav');
  if (existing) existing.remove();

  // Fetch and inject
  fetch(prefix + 'components/nav.html')
    .then(r => r.text())
    .then(html => {
      // Insert after body opens
      const temp = document.createElement('div');
      temp.innerHTML = html;
      const nav = temp.firstElementChild;

      // Set active states based on current path
      nav.querySelectorAll('a').forEach(link => {
        const href = link.getAttribute('href');
        if (href && path.startsWith(href) && href !== '/') {
          link.classList.add('active');
          // Also mark parent group active
          const group = link.closest('.whisper-group');
          if (group) {
            group.querySelector('.whisper-parent').classList.add('active');
          }
        }
      });

      document.body.appendChild(nav);
    })
    .catch(() => {
      // Silently fail — nav just won't show, page still works
    });
})();
