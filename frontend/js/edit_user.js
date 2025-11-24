import { buscarUsuario, buscarAvatar, customAlert } from "./funcoes.js";

const hash = window.location.hash;
const parts = hash.split("/");
const id = parts[2];


const user = await buscarUsuario(id);
console.log(user);

document.getElementById("name_edit").innerText = user.usuarios[0].apelido;
document.getElementById("assinatura_edit").value = user.usuarios[0].assinatura;
document.getElementById("biografia_edit").value = user.usuarios[0].biografia;
document.getElementById("user_id").value = user.usuarios[0].id;
document.getElementById("avatar_user_id").value = user.usuarios[0].id;
document.getElementById("avatar_edit").src = await buscarAvatar(user.usuarios[0].avatar_filename);

//salva as alterações de perfil
const btnSalvar = document.getElementById('save_edit');
btnSalvar.addEventListener('click', async () => {
    const user_id = document.getElementById('user_id').value;
    const name = document.getElementById('name_edit').value;
    const biografia = document.getElementById('biografia_edit').value;
    const assinatura = document.getElementById('assinatura_edit').value;

    if (name || biografia || assinatura) {
        const config = window.APP_CONFIG;

        if (!config) {
            customAlert('Erro ao carregar configuração do sistema.');
            return;
        }

        const host = config.database.host;
        const port = config.database.port;

        if (assinatura) {
            const apiUrl = `http://${host}:${port}/usuarios/${user_id}/editar/assinatura`;
            console.log("Tentando acessar:", apiUrl);

            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${sessionStorage.getItem('user_auth')}`
                },
                body: JSON.stringify({
                    assinatura: assinatura
                }),
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText || "Erro ao editar assinatura.");
            }
        }

        if (biografia) {
            const apiUrl = `http://${host}:${port}/usuarios/${user_id}/editar/biografia`;
            console.log("Tentando acessar:", apiUrl);

            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${sessionStorage.getItem('user_auth')}`
                },
                body: JSON.stringify({
                    texto: biografia
                }),
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText || "Erro ao editar biografia.");
            }
        }

        window.location.href = `#/visualizar/${user_id}`;
    }
});

const btnSalvarAvatar = document.getElementById('salvar_avatar');

btnSalvarAvatar.addEventListener('click', async () => {
    const user_id = document.getElementById('avatar_user_id').value;
    const avatarFile = document.getElementById('avatar').files[0];

    if (!avatarFile) {
        customAlert("Selecione uma imagem antes de salvar.");
        return;
    }

    const config = window.APP_CONFIG;
    if (!config) {
        customAlert('Erro ao carregar configuração do sistema.');
        return;
    }

    const host = config.database.host;
    const port = config.database.port;

    const apiUrl = `http://${host}:${port}/usuarios/${user_id}/editar/avatar`;
    console.log("Tentando acessar:", apiUrl);

    const formData = new FormData();
    formData.append("file", avatarFile);

    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${sessionStorage.getItem('user_auth')}`
        },
        body: formData,
    });

    console.log(response);

    if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || "Erro ao editar avatar.");
    }

    const meuModal = new bootstrap.Modal(document.getElementById('meuModal'));
    meuModal.hide();

    customcustomAlert("Sucesso", "Avatar alterado com sucesso.");
    window.location.href = `#/visualizar/${user_id}`;
});

