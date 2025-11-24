import { buscarAvatar, customAlert } from "./funcoes.js";
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
            customAlert('Erro ao carregar configuração do sistema.');
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
    member.classList.add('member', 'post', 'p-3', 'mb-3');

    member.innerHTML = `
        <div class="card shadow-sm border-0" style="border-radius: 12px;">
            <div class="card-body d-flex align-items-center">
                
                <!-- Avatar -->
                <div class="me-3">
                    <img src="${buscarAvatar(user.avatar_filename)}" 
                         class="rounded-circle border" 
                         style="width: 80px; height: 80px; object-fit: cover;">
                </div>

                <!-- Nome + link -->
                <div class="flex-grow-1">
                    <h5 class="mb-1">${user.apelido}</h5>
                    <a href="#/visualizar/${user.id}" class="text-primary" style="font-size: 0.9rem;">
                        Ver perfil →
                    </a>
                </div>

            </div>
        </div>
    `;

    sectionMembers.appendChild(member);
});

    } catch (error) {
        console.error('Erro ao carregar membros:', error);
    }
}   