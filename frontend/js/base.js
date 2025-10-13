// ====== CHECA AUTENTICAÇÃO PARA ENVIAR MENSAGEM NO CHAT ======
const chatForm = document.getElementById("chatForm");
const isAuthenticated = !!sessionStorage.getItem("user_auth");

if (chatForm) {
    console.log(isAuthenticated);

    if (!isAuthenticated) {
        chatForm.style.display = "none";

        const aviso = document.createElement("div");
        aviso.classList.add("text-muted", "text-center", "p-2", "small");
        aviso.textContent = "Faça login para enviar mensagens no chat.";
        chatForm.parentNode.insertBefore(aviso, chatForm);
    } else {
        chatForm.style.display = "block";
    }
}

console.log(isAuthenticated);

const panelUser = document.getElementById("panel-user");
const panelLogin = document.getElementById("panel-login");

if (isAuthenticated) {
    panelUser.hidden = false;
    panelLogin.hidden = true;
} else {
    panelUser.hidden = true;
    panelLogin.hidden = false;

    const btn = document.getElementById("sidebarLoginBtn");
    if (btn) {
        btn.addEventListener("click", () => {
            window.navigateTo("/login");
        });
    }
}

const registerLink = document.getElementById("register");
if (registerLink) {
    registerLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/register");
    });
}