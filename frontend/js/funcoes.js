export async function buscarUsuario(id) {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            alert('Erro ao carregar configuração do sistema.');
        }

        const host = config.database.host;
        const port = config.database.port;

        const paramsObj = {
            user_id: id,
            page: 1,
            size: 1,
        };

        const apiUrl = `http://${host}:${port}/usuarios/${paramsObj.user_id}?page=${paramsObj.page}&size=${paramsObj.size}`;
        console.log("Tentando acessar:", apiUrl);

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
        alert(error.message);
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
            alert('Erro ao carregar configuração do sistema.');
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
        alert(error.message);
    }
}

export async function buscarAllUsers() {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            alert('Erro ao carregar configuração do sistema.');
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
        alert(error.message);
    }
}

export async function buscarAllPostsByUser(id) {

    try {
        const config = window.APP_CONFIG;

        if (!config) {
            alert('Erro ao carregar configuração do sistema.');
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
        alert(error.message);
    }
}