const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const authStatus = document.getElementById('authStatus');

function goHome() {
  window.location.href = 'home.html';
}

if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const user = (document.getElementById('loginEmail')?.value || '').trim();
    const pass = (document.getElementById('loginPassword')?.value || '').trim();
    if (!user || !pass) {
      authStatus.textContent = 'Enter username and password.';
      return;
    }
    goHome();
  });
}

if (signupBtn) {
  signupBtn.addEventListener('click', () => {
    authStatus.textContent = 'Sign up form can be integrated with backend next.';
  });
}
