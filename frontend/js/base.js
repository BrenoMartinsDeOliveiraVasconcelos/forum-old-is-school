import { buscarUsuario, buscarAvatar} from "./funcoes.js";
// ====== CHECA AUTENTICAÇÃO PARA ENVIAR MENSAGEM NO CHAT ======
async function verificarAutenticacao() {
    const chatForm = document.getElementById("chatForm");
    const isAuthenticated = !!sessionStorage.getItem("user_auth");

    if (chatForm) {
        console.log(isAuthenticated);
        const avisoExistente = chatForm.previousElementSibling?.classList.contains("aviso-login");

        if (!isAuthenticated) {
            chatForm.style.display = "none";

            if (!avisoExistente) {
                const aviso = document.createElement("div");
                aviso.classList.add("aviso-login", "text-muted", "text-center", "p-2", "small");
                aviso.textContent = "Faça login para enviar mensagens no chat.";
                chatForm.parentNode.insertBefore(aviso, chatForm);
            }
        } else {
            chatForm.style.display = "block";
        }
    }


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
    const useName = document.getElementById("user-name");
    if (useName && isAuthenticated) {
        const userStr = sessionStorage.getItem('user');
        const user = JSON.parse(userStr);
        useName.textContent = user.apelido;
    }

    const sideAvatarImage = document.getElementById("user-avatar");
    if (sideAvatarImage && isAuthenticated) {
        const userStr = sessionStorage.getItem('user');
        const user = await buscarUsuario(JSON.parse(userStr).id);   
        
        sideAvatarImage.src = await buscarAvatar(user.usuarios[0].avatar_filename)
    }

    const divEditar = document.getElementById('editar_usuario');
    const userStr = sessionStorage.getItem('user');
    const user = JSON.parse(userStr);
    if (divEditar && user) {  
          
        divEditar.innerHTML = `
            <a href="#/editar_usuario/${user.id}">Editar</a><br>
            <a href="#/visualizar/${user.id}">Perfil</a>
        `;
    }
}

verificarAutenticacao();

setInterval(verificarAutenticacao, 1000);

const registerLink = document.getElementById("register");
if (registerLink) {
    registerLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/register");
    });
}

