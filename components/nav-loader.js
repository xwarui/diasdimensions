/* ============================================================
   nav-loader.js — fully qualified URL version
   ============================================================ */
(function() {
  var base = window.location.protocol + '//' + window.location.host;
  fetch(base + '/components/nav.html')
    .then(function(r) { return r.text(); })
    .then(function(html) {
      var temp = document.createElement('div');
      temp.innerHTML = html;
      var nav = temp.firstElementChild;

      var path = window.location.pathname;
      nav.querySelectorAll('a').forEach(function(link) {
        var href = link.getAttribute('href');
        if (href && href !== '/' && path.startsWith(href)) {
          link.classList.add('active');
          var group = link.closest('.whisper-group');
          if (group) {
            var parent = group.querySelector('.whisper-parent');
            if (parent) parent.classList.add('active');
          }
        }
      });

      document.body.appendChild(nav);
    })
    .catch(function() {});
})();
