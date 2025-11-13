// ====== CHECA AUTENTICAÇÃO PARA ENVIAR MENSAGEM NO CHAT ======
function verificarAutenticacao() {
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

async function dadosUsuario() {
    const userAuth = sessionStorage.getItem("user_auth");

    if (!userAuth) {
        console.log("Usuário não autenticado.");
        return;
    }

    try {
        const config = window.APP_CONFIG;
        if (!config || !config.database) {
            alert("Erro ao carregar configuração do sistema.");
            return;
        }

        const host = config.database.host;
        const port = config.database.port;

        // Aqui assumimos que userAuth guarda o ID do usuário logado
        const userId = userAuth;

        // Monta o endpoint correto: /usuarios/{user_id}
        const apiUrl = `http://${host}:${port}/usuarios/${userId}`;
        console.log("Buscando dados do usuário em:", apiUrl);

        // Faz a requisição GET — esse endpoint não usa body
        const response = await fetch(apiUrl, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || "Erro ao buscar dados do usuário.");
        }

        const data = await response.json();
        console.log("Dados completos do usuário:", data);

        // Aqui você pode exibir os dados na tela:
        const usuario = data.data || data; // depende de como api_response formata o retorno
        document.getElementById("userName").innerText = usuario.apelido;
        document.getElementById("userAvatar").src = usuario.avatar_filename
            ? `/uploads/${usuario.avatar_filename}`
            : "/img/default-avatar.png";

        // Se o endpoint também retorna posts/comentários:
        if (usuario.posts) {
            // renderizar os posts no DOM
            console.log("Posts do usuário:", usuario.posts);
        }

    } catch (error) {
        console.error("Erro ao buscar dados do usuário:", error);
        alert(error.message);
    }
}

dadosUsuario();

// setInterval(dadosUsuario, 1000);