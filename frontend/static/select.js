const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const utensilGrid = document.getElementById('utensilGrid');
const statusEl = document.getElementById('status');
const searchInput = document.getElementById('searchInput');
const chips = Array.from(document.querySelectorAll('.chip'));

let allProducts = [];
let activeFilter = 'all';

const SECTION_ORDER = [
  {
    key: 'core-cooking-vessels',
    products: [
      'Kadhai',
      'Frypan',
      'Saucepan',
      'Grill Pan',
      'Tawa',
      'Tasla',
      'Casserole / Handi',
      'Cooker',
    ],
  },
  {
    key: 'specialized-cookware',
    products: [
      'Appam Patra',
      'Multipurpose Pan',
      'Stock Pot',
      'Roasting Pan',
      'Baking Tray / Sheet',
    ],
  },
  {
    key: 'electric-utility',
    products: [
      'Electric Kettle',
      'Steamer / Puttu Maker',
      'Idli Stand',
    ],
  },
  {
    key: 'serving-mixing',
    products: ['Mixing Bowl', 'Serving Bowl / Handi'],
  },
  {
    key: 'indian-essentials',
    products: ['Chakla', 'Belan', 'Spice Box'],
  },
];

const SECTION_LABELS = {
  'core-cooking-vessels': 'Core Cooking Vessels',
  'specialized-cookware': 'Specialized Cookware',
  'electric-utility': 'Electric & Utility',
  'serving-mixing': 'Serving & Mixing',
  'indian-essentials': 'Indian Essentials',
};

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function normalizeName(name) {
  return (name || '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

function resolveSectionKey(name) {
  const normalized = normalizeName(name);
  for (const section of SECTION_ORDER) {
    if (section.products.some((p) => normalizeName(p) === normalized)) return section.key;
  }
  return null;
}

function orderedProducts(products) {
  const byName = new Map(products.map((p) => [normalizeName(p.name), p]));
  const used = new Set();
  const ordered = [];

  for (const section of SECTION_ORDER) {
    for (const productName of section.products) {
      const item = byName.get(normalizeName(productName));
      if (!item) continue;
      const key = item.id ? String(item.id) : normalizeName(item.name);
      if (used.has(key)) continue;
      used.add(key);
      ordered.push({ ...item, sectionKey: section.key });
    }
  }

  const fallback = products
    .filter((p) => {
      const key = p.id ? String(p.id) : normalizeName(p.name);
      return !used.has(key);
    })
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((p) => ({ ...p, sectionKey: resolveSectionKey(p.name) || 'all' }));

  return ordered.concat(fallback);
}

function healthScore(name) {
  let score = 70;
  if (/steel|triply|cast|iron/i.test(name)) score += 18;
  if (/non-stick|plastic/i.test(name)) score -= 8;
  return Math.max(58, Math.min(96, score));
}

function render(products) {
  const q = (searchInput?.value || '').trim().toLowerCase();
  const rows = orderedProducts(products).filter((p) => {
    const byChip = activeFilter === 'all' || p.sectionKey === activeFilter;
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
        <div class="badge">${SECTION_LABELS[p.sectionKey] || 'Other'}</div>
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
