const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const authStatus = document.getElementById('authStatus');

function goHome() {
  window.location.href = 'home.html';
}

if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const u = (document.getElementById('loginEmail')?.value || '').trim();
    const p = (document.getElementById('loginPassword')?.value || '').trim();
    if (!u || !p) {
      authStatus.textContent = 'Please enter username and password.';
      return;
    }
    goHome();
  });
}

if (signupBtn) {
  signupBtn.addEventListener('click', () => {
    authStatus.textContent = 'Sign up API can be connected next.';
  });
}
