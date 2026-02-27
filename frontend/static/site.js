(function initTopbar() {
  const toggle = document.getElementById('accountToggle');
  const menu = document.getElementById('authMenu');
  if (toggle && menu) {
    menu.classList.add('hidden');
    toggle.addEventListener('click', () => menu.classList.toggle('hidden'));
    document.addEventListener('click', (event) => {
      if (!menu.contains(event.target) && !toggle.contains(event.target)) {
        menu.classList.add('hidden');
      }
    });
  }

  const path = window.location.pathname;
  document.querySelectorAll('.navlinks a').forEach((link) => {
    const href = link.getAttribute('href') || '';
    const hrefNoExt = href.replace('.html', '');
    if (
      path.endsWith('/' + href) ||
      path === '/' + href ||
      path === href ||
      path === '/' + hrefNoExt
    ) {
      link.classList.add('active');
    }
  });
})();
