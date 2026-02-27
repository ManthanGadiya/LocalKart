const API_BASE = window.location.port === '63342' ? 'http://127.0.0.1:8000' : '';
const titleEl = document.getElementById('nearbyTitle');
const loadBtn = document.getElementById('loadNearbyBtn');
const tableBody = document.getElementById('shopsTableBody');
const useMyLocationBtn = document.getElementById('useMyLocationBtn');
const locationPreset = document.getElementById('locationPreset');
const locationStatus = document.getElementById('locationStatus');

let currentLat = 18.5204;
let currentLng = 73.8567;

async function fetchJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

function applyPreset() {
  const parts = (locationPreset.value || '').split(',');
  currentLat = Number(parts[0]);
  currentLng = Number(parts[1]);
  locationStatus.textContent = `Using preset location: ${locationPreset.options[locationPreset.selectedIndex].text}`;
}

function renderRows(rows) {
  if (!rows.length) {
    tableBody.innerHTML = '<tr><td colspan="4">No nearby shops found for this location.</td></tr>';
    return;
  }
  tableBody.innerHTML = rows
    .map((s) => `
      <tr>
        <td>${s.shop_name}</td>
        <td><a href="${s.maps_url || '#'}" target="_blank" rel="noreferrer">${s.address_line}, ${s.city}</a></td>
        <td>${s.phone ?? '-'}</td>
        <td>${s.rating ?? '-'}</td>
      </tr>
    `)
    .join('');
}

async function loadNearby() {
  const productId = localStorage.getItem('selectedProductId');
  const productName = localStorage.getItem('selectedProductName') || 'selected utensil';
  titleEl.textContent = `Showing stores for: ${productName}`;

  const params = new URLSearchParams({
    lat: String(currentLat),
    lng: String(currentLng),
    radius_km: '40',
  });
  if (productId) params.set('product_id', productId);

  const rows = await fetchJson(`${API_BASE}/api/shops/nearby?${params.toString()}`);
  renderRows(rows);
}

if (locationPreset) {
  locationPreset.addEventListener('change', () => {
    applyPreset();
  });
}

if (useMyLocationBtn) {
  useMyLocationBtn.addEventListener('click', () => {
    if (!navigator.geolocation) {
      locationStatus.textContent = 'Geolocation is not supported in this browser.';
      return;
    }
    locationStatus.textContent = 'Detecting your current location...';
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        currentLat = Number(pos.coords.latitude.toFixed(6));
        currentLng = Number(pos.coords.longitude.toFixed(6));
        locationStatus.textContent = `Using your location: ${currentLat}, ${currentLng}`;
        loadNearby().catch((e) => {
          tableBody.innerHTML = `<tr><td colspan="4">${e.message}</td></tr>`;
        });
      },
      () => {
        locationStatus.textContent = 'Location permission denied. Using selected preset.';
      },
      { enableHighAccuracy: true, timeout: 8000 }
    );
  });
}

loadBtn.addEventListener('click', () => {
  loadNearby().catch((e) => {
    tableBody.innerHTML = `<tr><td colspan="4">${e.message}</td></tr>`;
  });
});

applyPreset();
loadNearby().catch((e) => {
  tableBody.innerHTML = `<tr><td colspan="4">${e.message}</td></tr>`;
});
