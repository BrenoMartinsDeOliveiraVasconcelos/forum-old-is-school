const sectionMembers = document.getElementById('members-section');

if (sectionMembers) {
    carregarEExibirMembros(sectionMembers).catch(err => {
        console.error('Erro ao carregar membros:', err);
    });
}

async function carregarEExibirMembros(sectionMembers) {
    try {
        const config = window.APP_CONFIG;
        if (!config) {
            alert('Erro ao carregar configuração do sistema.');
            return;
        }
        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            page: 1,
            size: 100
        };

        const apiUrl = `http://${host}:${port}/usuarios?page=${paramsObj.page}&size=${paramsObj.size}`;
        console.log('Tentando acessar:', apiUrl);

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}` }
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || 'Erro ao carregar membros.');
        }

        const users = await response.json();
        console.log('users:', users);

        sectionMembers.innerHTML = "";

        users.usuarios.forEach(user => {
            const member = document.createElement('div');
            member.classList.add('member');
            member.classList.add('post');
            member.innerHTML = `
                <div class="row">
                <div class="member-avatar col-4">
                    <img src="${user.avatar || '/frontend/assets/img/user.svg'}" class="user-avatar"> <span class= "mr-4">${user.apelido}</span> 
                </div>
                <div class="row">
                 <a href="#/visualizar/${user.id}" class="text-end">Ver perfil</a>
                </div>
            `;
            sectionMembers.appendChild(member);
        });
    } catch (error) {
        console.error('Erro ao carregar membros:', error);
    }
}   