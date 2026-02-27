const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const titleEl = document.getElementById('nearbyTitle');
const loadBtn = document.getElementById('loadNearbyBtn');
const useMyLocationBtn = document.getElementById('useMyLocationBtn');
const locationPreset = document.getElementById('locationPreset');
const locationStatus = document.getElementById('locationStatus');
const storesGrid = document.getElementById('storesGrid');

let currentLat = 18.5204;
let currentLng = 73.8567;

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function applyPreset() {
  const [lat, lng] = (locationPreset.value || '').split(',').map(Number);
  currentLat = lat;
  currentLng = lng;
  locationStatus.textContent = `Preset active: ${locationPreset.options[locationPreset.selectedIndex].text}`;
}

function renderStores(rows) {
  if (!rows.length) {
    storesGrid.innerHTML = '<article class="store-card glass">No stores found for this area.</article>';
    return;
  }
  storesGrid.innerHTML = rows.map((s) => `
    <article class="store-card glass">
      <div class="store-thumb"></div>
      <h4>${s.shop_name}</h4>
      <p class="muted">${s.address_line}, ${s.city}</p>
      <p class="muted">Distance: ${s.distance_km} km | Rating: ${s.rating ?? '-'}</p>
      <a class="call-btn" href="tel:${s.phone ?? ''}">Call</a>
      <a class="btn btn-outline" href="${s.maps_url || '#'}" target="_blank" rel="noreferrer">Open Map</a>
    </article>
  `).join('');
}

async function loadNearby() {
  const productId = localStorage.getItem('selectedProductId');
  const productName = localStorage.getItem('selectedProductName') || 'selected utensil';
  titleEl.textContent = `Nearby stores for: ${productName}`;

  const params = new URLSearchParams({ lat: String(currentLat), lng: String(currentLng), radius_km: '45' });
  if (productId) params.set('product_id', productId);
  const rows = await fetchJson(`${API_BASE}/api/shops/nearby?${params.toString()}`);
  renderStores(rows.slice(0, 18));
}

if (locationPreset) locationPreset.addEventListener('change', applyPreset);

if (useMyLocationBtn) {
  useMyLocationBtn.addEventListener('click', () => {
    if (!navigator.geolocation) {
      locationStatus.textContent = 'Geolocation not supported. Using preset.';
      return;
    }
    locationStatus.textContent = 'Detecting current location...';
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentLat = Number(pos.coords.latitude.toFixed(6));
        currentLng = Number(pos.coords.longitude.toFixed(6));
        locationStatus.textContent = `Using current location: ${currentLat}, ${currentLng}`;
        loadNearby().catch((e) => {
          storesGrid.innerHTML = `<article class="store-card glass">${e.message}</article>`;
        });
      },
      () => { locationStatus.textContent = 'Location denied. Continuing with preset.'; },
      { timeout: 8000 }
    );
  });
}

if (loadBtn) {
  loadBtn.addEventListener('click', () => {
    loadNearby().catch((e) => {
      storesGrid.innerHTML = `<article class="store-card glass">${e.message}</article>`;
    });
  });
}

applyPreset();
loadNearby().catch((e) => {
  storesGrid.innerHTML = `<article class="store-card glass">${e.message}</article>`;
});
