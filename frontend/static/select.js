const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const utensilGrid = document.getElementById('utensilGrid');
const statusEl = document.getElementById('status');
const searchInput = document.getElementById('searchInput');
const chips = Array.from(document.querySelectorAll('.chip'));

let allProducts = [];
let activeFilter = 'all';

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function classifyProduct(p) {
  const n = p.name.toLowerCase();
  if (n.includes('jar') || n.includes('box') || n.includes('rack') || n.includes('bin') || n.includes('container')) return 'storage';
  if (n.includes('kettle') || n.includes('air fryer') || n.includes('mixer') || n.includes('blender') || n.includes('toaster') || n.includes('cooker')) return 'appliances';
  return 'cookware';
}

function healthScore(name) {
  let score = 70;
  if (/steel|triply|cast|iron/i.test(name)) score += 18;
  if (/non-stick|plastic/i.test(name)) score -= 8;
  return Math.max(58, Math.min(96, score));
}

function render(products) {
  const q = (searchInput?.value || '').trim().toLowerCase();
  const rows = products.filter((p) => {
    const cat = classifyProduct(p);
    const byChip = activeFilter === 'all' || cat === activeFilter;
    const bySearch = !q || p.name.toLowerCase().includes(q);
    return byChip && bySearch;
  });

  if (!rows.length) {
    utensilGrid.innerHTML = '';
    statusEl.textContent = 'No utensils match your search/filter.';
    return;
  }

  statusEl.textContent = '';
  utensilGrid.innerHTML = rows
    .map((p, i) => {
      const score = healthScore(p.name);
      return `
      <article class="utensil-card glass" data-id="${p.id}" data-name="${p.name}">
        <span class="rating-dot" title="rating"></span>
        <div class="thumb">${p.name}</div>
        <strong>${p.name}</strong>
        <div class="health-badge">Health Score: ${score}</div>
      </article>`;
    })
    .join('');

  utensilGrid.querySelectorAll('.utensil-card').forEach((card) => {
    card.addEventListener('click', () => {
      localStorage.setItem('selectedProductId', card.dataset.id || '');
      localStorage.setItem('selectedProductName', card.dataset.name || '');
      window.location.href = 'materials.html';
    });
  });
}

async function init() {
  const categories = await fetchJson(`${API_BASE}/api/categories`);
  const productsByCategory = await Promise.all(
    categories.map((c) => fetchJson(`${API_BASE}/api/products?category_id=${c.id}`))
  );
  allProducts = productsByCategory.flat();
  render(allProducts);
}

chips.forEach((chip) => {
  chip.addEventListener('click', () => {
    chips.forEach((c) => c.classList.remove('active'));
    chip.classList.add('active');
    activeFilter = chip.dataset.filter || 'all';
    render(allProducts);
  });
});

if (searchInput) {
  searchInput.addEventListener('input', () => render(allProducts));
}

init().catch((e) => {
  statusEl.textContent = e.message;
});
