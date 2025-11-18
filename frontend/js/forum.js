const newPostLink = document.getElementById("btn-new-post");
console.log(newPostLink);

if (newPostLink) {
    newPostLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/novo_post");
    });
}

const postagens = document.querySelectorAll(".post");

try {
    const config = window.APP_CONFIG;

    if (!config) {
        alert("Erro ao carregar configuração do sistema.");
    }

    const host = config.database.host;
    const port = config.database.port;

    const paramsObj = {
        page: 1,
        page_size: 10,
        categoria_id: 1
    };

    // Monta a URL com parâmetros GET
    const apiUrl = `http://${host}:${port}/posts?page=${paramsObj.page}&page_size=${paramsObj.page_size}&categoria_id=${paramsObj.categoria_id}`;
    console.log("Tentando acessar:", apiUrl);

    // Faz o GET sem body (GET não aceita body no navegador)
    const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('user_auth')}`
        }
    });

    // Log da resposta
    console.log("Status:", response.status);

    if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText || "Erro ao carregar postagens.");
    }

    const posts = await response.json();
    console.log("Postagens:", posts);

} catch (error) {
    console.error("Erro ao carregar postagens:", error);
    alert(error.message);
}


// var xhr = new XMLHttpRequest();
// var url = "url?data=" + encodeURIComponent(JSON.stringify({"email": "hey@mail.com", "password": "101010"}));
// xhr.open("GET", url, true);
// xhr.setRequestHeader("Content-Type", "application/json");
// xhr.onreadystatechange = function () {
//     if (xhr.readyState === 4 && xhr.status === 200) {
//         var json = JSON.parse(xhr.responseText);
//         console.log(json.email + ", " + json.password);
//     }
// };
// xhr.send();