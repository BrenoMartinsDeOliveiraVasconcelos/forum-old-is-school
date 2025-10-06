function initLogin() {
        history.pushState({}, '', '/dashboard');
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        // mock: aceita qualquer credencial
        sessionStorage.setItem('auth', '1');
        // redireciona para dashboard sem expor caminho do arquivo
        history.pushState({}, '', '/dashboard');
        window.dispatchEvent(new PopStateEvent('popstate'));
    });
}