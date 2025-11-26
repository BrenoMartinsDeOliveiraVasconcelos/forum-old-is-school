import { customAlert } from "./funcoes.js";
const btnCadastrar = document.getElementById('cadastrar-post');


btnCadastrar.addEventListener('click', async (e) => {
    e.preventDefault();

    const title = document.getElementById('title').value.trim();
    const category = document.getElementById('categoria').value.trim();
    const content = document.getElementById('conteudo_new_post').value.trim();

    if (!title || !category || !content) {
        customAlert('Preencha todos os campos!');
        return;
    }

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
            return;
        }

        const host = config.database.host;
        const port = config.database.port;

        const apiUrl = `http://${host}:${port}/posts`;
        console.log('Tentando acessar:', apiUrl);

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}`,
            },
            body: JSON.stringify({
                titulo: title,
                categoria_id: category,
                conteudo: content
            }),
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || 'Erro ao cadastrar post.');
        }

        const data = await response.json();

        window.navigateTo('/forum');
    } catch (error) {
        console.error('Erro ao cadastrar post:', error);
        customAlert("Erro ao cadastrar post.", error.message);
    }


});
