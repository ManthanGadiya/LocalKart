function applyTheme(theme) {
  const body = document.body;
  if (!body) return;
  body.classList.toggle('light', theme === 'light');
  localStorage.setItem('localkart-theme', theme);
}

(function initSite() {
  const savedTheme = localStorage.getItem('localkart-theme') || 'dark';
  applyTheme(savedTheme);

  const toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const next = document.body.classList.contains('light') ? 'dark' : 'light';
      applyTheme(next);
    });
  }

  const path = window.location.pathname;
  document.querySelectorAll('.navlinks a').forEach((link) => {
    const href = link.getAttribute('href') || '';
    if (path.endsWith('/' + href) || path === '/' + href || path === href) {
      link.classList.add('active');
    }
  });

  document.querySelectorAll('.navlinks a[href="index.html"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      localStorage.removeItem('localkart-user');
      localStorage.removeItem('selectedProductId');
      localStorage.removeItem('selectedProductName');
      window.location.href = '/';
    });
  });

  const particlesHost = document.querySelector('.particles');
  if (particlesHost) {
    for (let i = 0; i < 36; i++) {
      const dot = document.createElement('span');
      dot.style.left = `${Math.random() * 100}%`;
      dot.style.bottom = `${-10 - Math.random() * 40}px`;
      dot.style.animationDuration = `${7 + Math.random() * 10}s`;
      dot.style.animationDelay = `${Math.random() * 8}s`;
      particlesHost.appendChild(dot);
    }
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('show');
      });
    },
    { threshold: 0.15 }
  );
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  const loader = document.getElementById('globalLoader');
  window.addEventListener('load', () => {
    document.body.classList.add('ready');
    if (loader) loader.classList.add('hidden');
  });

  const fab = document.getElementById('compareFab');
  if (fab) {
    fab.addEventListener('click', () => {
      window.location.href = 'nearby.html';
    });
  }
})();
