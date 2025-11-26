export async function buscarUsuario(id) {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            user_id: id,
            page: 1,
            size: 1,
        };

        const apiUrl = `http://${host}:${port}/usuarios/${paramsObj.user_id}?page=${paramsObj.page}&size=${paramsObj.size}`;

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}`
            }
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || 'Erro ao carregar autor.');
        }

        const autor = await response.json();

        return autor
    } catch (error) {
        console.error('Erro ao carregar autor:', error);
        customAlert(error.message);
    }
}

export function formatarData(dataString) {
    const data = new Date(dataString);

    const dia = String(data.getDate()).padStart(2, "0");
    const mes = String(data.getMonth() + 1).padStart(2, "0");
    const ano = data.getFullYear();

    const horas = String(data.getHours()).padStart(2, "0");
    const minutos = String(data.getMinutes()).padStart(2, "0");

    return `${dia}/${mes}/${ano} ${horas}:${minutos}`;
}

export async function buscarPost(id) {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            post_id: id,
        };

        const apiUrl = `http://${host}:${port}/posts/${paramsObj.post_id}`;
        console.log("Tentando acessar:", apiUrl);

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}`
            }
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || 'Erro ao carregar post.');
        }

        const post = await response.json();

        return post
    } catch (error) {
        console.error('Erro ao carregar post:', error);
        customAlert(error.message);
    }
}

export async function buscarAllUsers() {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            page: 1,
            size: 100,
        };

        const apiUrlUser = `http://${host}:${port}/usuarios?page=${paramsObj.page}&size=${paramsObj.size}`;
        const user = await fetch(apiUrlUser, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        const userData = await user.json();

        return userData
    } catch (error) {
        console.error('Erro ao carregar autor:', error);
        customAlert(error.message);
    }
}

export async function buscarAllPostsByUser(id) {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            user_id: id,
            page: 1,
            size: 100,
        };

        const apiUrlUser = `http://${host}:${port}/usuarios/${paramsObj.user_id}/posts?page=${paramsObj.page}&size=${paramsObj.size}`;
        const user = await fetch(apiUrlUser, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        const userData = await user.json();

        return userData
    } catch (error) {
        console.error('Erro ao carregar autor:', error);
        customAlert(error.message);
    }
}

export function buscarAvatar(file) {

    const config = window.APP_CONFIG;

    if (!config) {
        customAlert('Erro ao carregar configuração do sistema.');
        return;
    }

    const host = config.database.host;
    const port = config.database.port;

    if (!file) {
        return `/frontend/assets/img/user.svg`;
    }

    return `http://${host}:${port}/arquivos/avatares/${file}`;
}

export function customAlert(titulo, mensagem) {
    const overlay = document.createElement("div");
    overlay.className = "custom-alert-overlay";

    const errorMessages = {
        "Item ja cadastrado": "Já existe cadastro no sistema.",
        "Incorrect username or password": "Nome de usuário ou senha incorretos.",
        "Usuário já existe": "Já existe um usuário cadastrado com estes dados.",
        "Token inválido": "Sua sessão expirou, faça login novamente.",
        "Not authenticated": "Você precisa estar autenticado para realizar esta ação.",
        "database error": "Houve um problema ao salvar no servidor. Tente novamente mais tarde."
    };
    let mensagemClara = mensagem;

    try {
        const parsed = JSON.parse(mensagem);        

        if (parsed.detail) {
            let encontrada = Object.keys(errorMessages)
                .find(key => parsed.detail.includes(key));            

            if (encontrada) {
                mensagemClara = errorMessages[encontrada];
            } else {
                mensagemClara = parsed.detail;
            }
        }
    } catch (error) {
        console.error(error);
    }

    overlay.innerHTML = `
        <div class="custom-alert-box">
            <h2>${titulo}</h2>
            <p>${mensagemClara}</p>
            <button class="custom-alert-btn">OK</button>
        </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector("button").onclick = () => {
        overlay.remove();
    };
}