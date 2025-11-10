const form = document.getElementById('sidebarLoginForm');
console.log(form);

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
            console.log(host, port);

            const apiUrl = `http://${host}:${port}/token`;
            console.log('Tentando acessar:', apiUrl);

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: JSON.stringify({
                    apelido: username,
                    senha: password
                }),
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText || 'Erro ao fazer login.');
            }

            const data = await response.json();
            console.log(data);

            sessionStorage.setItem('user_auth', data.token);
            window.navigateTo('/dashboard');
        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    });
}