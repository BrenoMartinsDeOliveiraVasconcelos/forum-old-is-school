/* CHAMADA DA TELA DE LOGIN */
function setupLoginButton() {
    const btnLogin = document.getElementById('loginBtn');
    if (!btnLogin) return; // evita erro se o botão não existir

    btnLogin.addEventListener('click', () => {
        // Altera o hash para disparar o router
        // window.location.hash = '#/login';
        // ou se você quer usar history.pushState:
        history.pushState({}, '', '/login');
        window.dispatchEvent(new PopStateEvent('popstate'));
    });
}

// Chame essa função após o DOM estar carregado
document.addEventListener('DOMContentLoaded', () => {
    setupLoginButton();
});