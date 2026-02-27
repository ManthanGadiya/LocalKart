const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const utensilGrid = document.getElementById('utensilGrid');
const statusEl = document.getElementById('status');

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function utensilIcon(name) {
  const n = name.toLowerCase();
  if (n.includes('kadhai')) return 'Pan';
  if (n.includes('frying')) return 'Fry';
  if (n.includes('tawa')) return 'Tawa';
  if (n.includes('cooker')) return 'Cook';
  return 'Utensil';
}

function renderProducts(products) {
  utensilGrid.innerHTML = products
    .map(
      (p) => `
      <article class="utensil-card" data-id="${p.id}" data-name="${p.name}">
        <strong>${utensilIcon(p.name)} - ${p.name}</strong>
      </article>
    `
    )
    .join('');

  utensilGrid.querySelectorAll('.utensil-card').forEach((card) => {
    card.addEventListener('click', () => {
      utensilGrid.querySelectorAll('.utensil-card').forEach((c) => c.classList.remove('selected'));
      card.classList.add('selected');
      localStorage.setItem('selectedProductId', card.dataset.id || '');
      localStorage.setItem('selectedProductName', card.dataset.name || '');
      window.location.href = 'materials.html';
    });
  });
}

async function init() {
  const categories = await fetchJson(`${API_BASE}/api/categories`);
  const utensils = categories.find((c) => c.name.toLowerCase() === 'utensils');
  if (!utensils) {
    statusEl.textContent = 'Utensils category not found.';
    return;
  }
  const products = await fetchJson(`${API_BASE}/api/products?category_id=${utensils.id}`);
  renderProducts(products.slice(0, 12));
}

init().catch((e) => {
  statusEl.textContent = e.message;
});
