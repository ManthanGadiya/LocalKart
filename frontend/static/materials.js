const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const productNameEl = document.getElementById('selectedProduct');
const cardsEl = document.getElementById('materialsCards');

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function featureText(features, type) {
  return (features || [])
    .filter((f) => f.feature_type === type)
    .map((f) => f.feature_text)
    .join('; ') || '-';
}

function renderCards(rows) {
  cardsEl.innerHTML = rows
    .map((r) => {
      const pro = featureText(r.features, 'pro');
      const con = featureText(r.features, 'con');
      const general = featureText(r.features, 'general');
      return `
        <article class="material-card">
          <h3>${r.material}</h3>
          <p class="ok">+ ${pro}</p>
          <p class="bad">- ${con}</p>
          <p><strong>Health:</strong> ${general}</p>
          <p><strong>Best For:</strong> Regular cooking</p>
          <p><strong>Price:</strong> ${r.min_price ?? '-'} - ${r.max_price ?? '-'}</p>
        </article>
      `;
    })
    .join('');
}

async function init() {
  const productId = localStorage.getItem('selectedProductId');
  const productName = localStorage.getItem('selectedProductName');
  if (!productId) {
    productNameEl.textContent = 'No utensil selected. Go back and choose one.';
    cardsEl.innerHTML = '';
    return;
  }
  productNameEl.textContent = `Selected Utensil: ${productName || productId}`;
  const rows = await fetchJson(`${API_BASE}/api/products/${productId}/varieties`);
  renderCards(rows.slice(0, 4));
}

init().catch((e) => {
  cardsEl.innerHTML = `<article class="material-card">${e.message}</article>`;
});
