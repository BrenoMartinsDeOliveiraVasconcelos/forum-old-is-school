import { customAlert, formatarData } from "./funcoes.js";
const chat = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const chatText = document.getElementById("chatText");

const usuarioLogadoStr = sessionStorage.getItem("user");
const usuarioLogado = JSON.parse(usuarioLogadoStr);

let ultimoId = 0;
// 🔄 Carregar mensagens
async function carregarMensagens() {
    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
            return;
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = { page: 1, size: 10 };

        const res = await fetch(`http://${host}:${port}/mensagens?page=${paramsObj.page}&size=${paramsObj.size}`);

        if (!res.ok) {
            console.error("Erro ao buscar mensagens");
            return;
        }

        const mensagens = await res.json();
        console.log(mensagens);

        renderizarChatSemPiscar(mensagens);
    } catch (err) {
        console.error("Erro:", err);
    }
}


function renderizarChatSemPiscar(lista) {
    lista.forEach(msg => {
        if (msg.id <= ultimoId) return;

        const div = document.createElement("div");
        div.classList.add("message");
        if (usuarioLogado) {
            div.classList.add(msg.autor_id === usuarioLogado.id ? "self" : "other");
            div.classList.add(msg.autor_id === usuarioLogado.id ? "text-end" : "text-start");
        } else {
            div.classList.add("other");
            div.classList.add("text-start");
        }

        div.innerHTML = `<b>${formatarData(msg.timestamp)} - ${msg.autor.apelido}:</b><br> ${msg.mensagem}`;

        chat.appendChild(div);

        ultimoId = msg.id;
    });

    chat.scrollTop = chat.scrollHeight;
}

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const texto = chatText.value.trim();
    if (!texto) return;

    const payload = {
        mensagem: texto
    };

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
            return;
        }

        const host = config.database.host;
        const port = config.database.port;

        await fetch(`http://${host}:${port}/mensagens`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${sessionStorage.getItem('user_auth')}`
            },
            body: JSON.stringify(payload),
        });

        chatText.value = "";
        carregarMensagens();

    } catch (err) {
        console.error(err);
    }
});

// 🔄 Atualiza o chat automaticamente a cada 2s
setInterval(carregarMensagens, 2000);

// Carrega no início
carregarMensagens();
