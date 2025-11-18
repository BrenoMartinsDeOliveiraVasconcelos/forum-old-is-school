const form = document.getElementById('sidebarLoginForm');

if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value.trim();

        if (!username || !password) {
            alert('Preencha todos os campos!');
            return;
        }

        try {
            const config = window.APP_CONFIG;

            if (!config) {
                alert('Erro ao carregar configuração do sistema.');
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

            const apiUrlUser = `http://${host}:${port}/usuarios`;
            const user = await fetch(apiUrlUser, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            const userData = await user.json();
            console.log(userData);
            
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
        window.navigateTo('/dashboard');
    });
}