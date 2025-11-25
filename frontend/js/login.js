import { customAlert } from "./funcoes.js";

const form = document.getElementById('sidebarLoginForm');

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value.trim();

        if (!username || !password) {
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

            const body = new URLSearchParams();
            body.append('username', username);
            body.append('password', password);

            const apiUrl = `http://${host}:${port}/token`;
            console.log('Tentando acessar:', apiUrl);

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: body,
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText || 'Erro ao fazer login.');
            }

            const data = await response.json();

            sessionStorage.setItem('user_auth', data.access_token);
            document.getElementById('loginUsername').value = '';
            document.getElementById('loginPassword').value = '';
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
            console.log(userData);

            // Encontra o usuário cujo apelido é igual ao username digitado
            const usuarioEncontrado = userData.usuarios.find(u => u.apelido === username);

            if (usuarioEncontrado) {
                // Salva no sessionStorage como STRING
                sessionStorage.setItem('user', JSON.stringify(usuarioEncontrado));

                const divEditar = document.getElementById('editar_usuario');
                if (divEditar) {
                    divEditar.innerHTML = `
                        <a href="#/editar_usuario/${usuarioEncontrado.id}?page=1&size=1">Editar</a><br>
                        <a href="#/visualizar/${user.id}">Perfil</a>
                    `;
                }

            } else {
                console.warn("Nenhum usuário encontrado com esse apelido.");
            }

            window.location.reload();
            window.navigateTo('/dashboard');
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    });
}

const logout = document.getElementById('logout');
if (logout) {
    logout.addEventListener('click', () => {
        sessionStorage.removeItem('user_auth');
        sessionStorage.removeItem('user');
        window.location.reload();
        window.navigateTo('/dashboard');
    });
}