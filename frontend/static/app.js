const categorySelect = document.getElementById("categorySelect");
const productSelect = document.getElementById("productSelect");
const latInput = document.getElementById("latInput");
const lngInput = document.getElementById("lngInput");
const loadVarietiesBtn = document.getElementById("loadVarietiesBtn");
const nearbyShopsBtn = document.getElementById("nearbyShopsBtn");
const varietiesList = document.getElementById("varietiesList");
const shopsList = document.getElementById("shopsList");
const API_BASE =
  window.LOCALKART_API_BASE ||
  (window.location.port === "63342" ? "http://127.0.0.1:8000" : "");

const isDiscoverPage =
  categorySelect &&
  productSelect &&
  latInput &&
  lngInput &&
  loadVarietiesBtn &&
  nearbyShopsBtn &&
  varietiesList &&
  shopsList;

if (!isDiscoverPage) {
  // Keep this file safe to include on any page.
} else {

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function renderBox(el, html) {
  el.innerHTML = html;
}

async function loadCategories() {
  const categories = await fetchJson(`${API_BASE}/api/categories`);
  for (const c of categories) {
    const op = document.createElement('option');
    op.value = c.id;
    op.textContent = c.name;
    categorySelect.appendChild(op);
  }
}

async function loadProducts() {
  const cid = categorySelect.value;
  const q = cid ? `?category_id=${encodeURIComponent(cid)}` : '';
  const products = await fetchJson(`${API_BASE}/api/products${q}`);
  productSelect.innerHTML = '<option value="">Select product</option>';
  for (const p of products) {
    const op = document.createElement('option');
    op.value = p.id;
    op.textContent = p.name;
    productSelect.appendChild(op);
  }
}

categorySelect.addEventListener('change', async () => {
  await loadProducts();
});

loadVarietiesBtn.addEventListener('click', async () => {
  if (!productSelect.value) {
    renderBox(varietiesList, '<div class="subtle">Select a product first.</div>');
    return;
  }
  const rows = await fetchJson(`${API_BASE}/api/products/${productSelect.value}/varieties`);
  if (!rows.length) {
    renderBox(varietiesList, '<div class="subtle">No varieties found.</div>');
    return;
  }
  renderBox(
    varietiesList,
    rows.map(r => `
      <div class="item">
        <strong>${r.display_name}</strong>
        <div class="subtle">Material: ${r.material}</div>
        <div class="subtle">Price: ${r.min_price ?? '-'} - ${r.max_price ?? '-'}</div>
        <div class="subtle">Score: ${r.recommendation_score ?? '-'}</div>
      </div>
    `).join('')
  );
});

nearbyShopsBtn.addEventListener('click', async () => {
  const lat = Number(latInput.value);
  const lng = Number(lngInput.value);
  if (Number.isNaN(lat) || Number.isNaN(lng)) {
    renderBox(shopsList, '<div class="subtle">Enter valid coordinates.</div>');
    return;
  }
  const params = new URLSearchParams({ lat: String(lat), lng: String(lng), radius_km: '10' });
  if (productSelect.value) params.set('product_id', productSelect.value);

  const rows = await fetchJson(`${API_BASE}/api/shops/nearby?${params.toString()}`);
  if (!rows.length) {
    renderBox(shopsList, '<div class="subtle">No nearby shops found.</div>');
    return;
  }

  renderBox(
    shopsList,
    rows.map(s => `
      <div class="item">
        <strong>${s.shop_name}</strong>
        <div class="subtle">${s.address_line}, ${s.city}</div>
        <div class="subtle">Distance: ${s.distance_km} km</div>
        <div class="subtle">Rating: ${s.rating ?? '-'}</div>
        ${s.maps_url ? `<a href="${s.maps_url}" target="_blank" rel="noreferrer">Open in Maps</a>` : ''}
      </div>
    `).join('')
  );
});

async function init() {
  renderBox(varietiesList, '<div class="subtle">Select product and click Load Varieties.</div>');
  renderBox(shopsList, '<div class="subtle">Enter location and click Find Nearby Shops.</div>');
  await loadCategories();
  await loadProducts();
}

init();
}
