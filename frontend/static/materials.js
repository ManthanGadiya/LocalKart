const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const selectedProductEl = document.getElementById('selectedProduct');
const tabsEl = document.getElementById('materialTabs');
const dashboardEl = document.getElementById('materialDashboard');

let materials = [];
let activeIndex = 0;

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function fText(features, type) {
  return (features || []).filter((f) => f.feature_type === type).map((f) => f.feature_text).join('; ') || '-';
}

function metricValue(seed) {
  return Math.max(20, Math.min(95, seed));
}

function renderDashboard(item) {
  const heat = metricValue(60 + (item.recommendation_score || 0) * 3);
  const durability = metricValue(55 + (item.recommendation_score || 0) * 3.4);
  const toxicRisk = metricValue(100 - (item.recommendation_score || 0) * 6);
  dashboardEl.innerHTML = `
    <div class="metric"><label>Heat Resistance</label><div class="bar"><div class="bar-fill" style="width:${heat}%"></div></div></div>
    <div class="metric"><label>Durability</label><div class="bar"><div class="bar-fill" style="width:${durability}%"></div></div></div>
    <div class="metric"><label>Toxic Risk</label><div class="bar"><div class="bar-fill" style="width:${toxicRisk}%"></div></div></div>
    <p><span class="badge">Price Level: ${item.min_price ?? '-'} - ${item.max_price ?? '-'}</span></p>
    <p><strong>Best For:</strong> ${fText(item.features, 'general')}</p>
    <p><strong>Pros:</strong> ${fText(item.features, 'pro')}</p>
    <p><strong>Cons:</strong> ${fText(item.features, 'con')}</p>
  `;
}

function renderTabs() {
  tabsEl.innerHTML = materials
    .map((m, idx) => `<button class="mat-tab ${idx===activeIndex?'active':''}" data-idx="${idx}" type="button">${m.material}</button>`)
    .join('');

  tabsEl.querySelectorAll('.mat-tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      activeIndex = Number(btn.dataset.idx || 0);
      renderTabs();
      renderDashboard(materials[activeIndex]);
    });
  });
}

async function init() {
  const productId = localStorage.getItem('selectedProductId');
  const productName = localStorage.getItem('selectedProductName') || 'Utensil';
  if (!productId) {
    selectedProductEl.textContent = 'No selected utensil. Go to Compare page first.';
    return;
  }
  selectedProductEl.textContent = `Selected: ${productName}`;
  materials = await fetchJson(`${API_BASE}/api/products/${productId}/varieties`);
  materials = materials.slice(0, 4);
  if (!materials.length) {
    dashboardEl.innerHTML = 'No material variants found.';
    return;
  }
  renderTabs();
  renderDashboard(materials[0]);
}

init().catch((e) => {
  selectedProductEl.textContent = e.message;
});
