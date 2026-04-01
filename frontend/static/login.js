const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const authStatus = document.getElementById('authStatus');
const API_BASE =
  window.LOCALKART_API_BASE ||
  (window.location.port === '63342' ? 'http://127.0.0.1:8000' : '');

async function postJson(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || `Request failed: ${res.status}`);
  return data;
}

function goHome(user) {
  if (user) {
    localStorage.setItem('localkart-user', JSON.stringify(user));
  }
  window.location.href = 'home.html';
}

if (loginBtn) {
  loginBtn.addEventListener('click', async () => {
    const email = (document.getElementById('loginEmail')?.value || '').trim().toLowerCase();
    const password = (document.getElementById('loginPassword')?.value || '').trim();
    if (!email || !password) {
      authStatus.textContent = 'Please enter email and password.';
      return;
    }

    authStatus.textContent = 'Checking credentials...';
    try {
      const data = await postJson(`${API_BASE}/api/login`, { email, password });
      authStatus.textContent = data.message || 'Login successful.';
      goHome(data.user);
    } catch (error) {
      authStatus.textContent = error.message;
    }
  });
}

if (signupBtn) {
  signupBtn.addEventListener('click', async () => {
    const email = (document.getElementById('loginEmail')?.value || '').trim().toLowerCase();
    const password = (document.getElementById('loginPassword')?.value || '').trim();
    if (!email || !password) {
      authStatus.textContent = 'Enter email and password to sign up.';
      return;
    }

    authStatus.textContent = 'Creating your account...';
    try {
      const data = await postJson(`${API_BASE}/api/signup`, { email, password });
      authStatus.textContent = data.message || 'Sign up successful.';
      goHome(data.user);
    } catch (error) {
      authStatus.textContent = error.message;
    }
  });
}
