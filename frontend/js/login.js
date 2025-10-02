document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const resposta = await fetch("http://127.0.0.1:8000/token", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });

        if (!resposta.ok) {
            document.getElementById("mensagem").textContent = "Usuário ou senha incorretos!";
            return;
        }

        const dados = await resposta.json();

        // Salvar token no localStorage
        localStorage.setItem("token", dados.access_token);

        document.getElementById("mensagem").textContent = "Login realizado com sucesso!";
        
        // Redirecionar para a página principal
        window.location.href = "index.html";
    } catch (error) {
        document.getElementById("mensagem").textContent = "Erro na conexão com o servidor.";
    }
});
