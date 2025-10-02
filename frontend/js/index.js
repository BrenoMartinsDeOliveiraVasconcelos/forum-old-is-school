async function listarUsuarios() {
    const token = localStorage.getItem("token");

    const resposta = await fetch("http://127.0.0.1:8000/usuarios", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    if (resposta.status === 401) {
        alert("Sessão expirada. Faça login novamente.");
        window.location.href = "login.html";
        return;
    }

    const usuarios = await resposta.json();
    let lista = document.getElementById("usuarios");
    lista.innerHTML = "";

    usuarios.forEach(u => {
        let li = document.createElement("li");
        li.textContent = u.nome;
        lista.appendChild(li);
    });
}
