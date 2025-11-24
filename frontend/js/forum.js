window.forumInitialized = false;

import { buscarUsuario, formatarData, customAlert } from "/frontend/js/funcoes.js";

window.onViewLoaded = function (view) {
    if (view !== "forum") return;

    if (window.forumInitialized) {
        console.log("Forum já inicializado — ignorando");
        return;
    }

    window.forumInitialized = true;
    initForum();
};

function initForum() {
    // garante que o DOM da view já existe
    const postsSection = document.getElementById("posts-section");
    if (!postsSection) return;

    console.log("Inicializando forum (initForum)");

    // evita duplicação visual: limpa antes de popular
    postsSection.innerHTML = "";

    // botão novo post: evita adicionar listener mais de uma vez
    const newPostLink = document.getElementById("btn-new-post");
    if (newPostLink && !newPostLink.dataset.listenerAdded) {
        newPostLink.addEventListener("click", (e) => {
            e.preventDefault();
            window.navigateTo("/novo_post");
        });
        newPostLink.dataset.listenerAdded = "1";
    }

    // carrega posts (async)
    carregarEExibirPosts(postsSection).catch(err => {
        console.error("Erro ao carregar posts:", err);
    });
}

async function carregarEExibirPosts(postsSection) {
    try {
        const config = window.APP_CONFIG;
        if (!config) {
            customAlert("Erro ao carregar configuração do sistema.");
            return;
        }
        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = { page: 1, size: 10, categoria_id: 1 };
        const apiUrl = `http://${host}:${port}/posts?page=${paramsObj.page}&size=${paramsObj.size}&categoria_id=${paramsObj.categoria_id}`;
        console.log("Tentando acessar:", apiUrl);

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}` }
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || "Erro ao carregar postagens.");
        }

        const posts = await response.json();
        posts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        console.log('posts:', posts);

        // garante limpar novamente (por segurança) antes de inserir
        postsSection.innerHTML = "";

        for (const post of posts) {
            const autor = await buscarUsuario(post.autor_id);
            console.log(autor);

            const postElement = document.createElement("div");
            postElement.classList.add("post");

            const dataFormatada = formatarData(post.timestamp);

            postElement.innerHTML = `
                <h3>${post.titulo}</h3>
                <p class="post-meta">Postado por <b>${autor?.usuarios?.[0]?.apelido || "Desconhecido"}</b> em ${dataFormatada}</p>
                <a href="#/posts/${post.id}" class="post-link text-end d-block">Visualizar >></a>
            `;

            postsSection.appendChild(postElement);
        }

        console.log("Posts renderizados. total:", postsSection.children.length);
    } catch (error) {
        console.error(error);
        throw error;
    }
}