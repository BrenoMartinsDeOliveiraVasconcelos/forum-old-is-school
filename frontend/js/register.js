import { customAlert } from "./funcoes.js";
const form = document.getElementById("registerForm");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            customAlert("As senhas não conferem!");
            return;
        }

        if (!username || !password || !confirmPassword) {
            customAlert("Preencha todos os campos!");
            return;
        }
        
        try {
            const config = window.APP_CONFIG;

            if (!config) {
                customAlert("Erro ao carregar configuração do sistema.");
                return;
            }

            const host = config.database.host;
            const port = config.database.port;
            console.log(host, port);
            

            const apiUrl = `http://${host}:${port}/usuarios`;
            console.log("Tentando acessar:", apiUrl);

            const response = await fetch(apiUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    apelido: username,
                    senha: password
                }),
            });

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText || "Erro ao cadastrar usuário.");
            }

            const data = await response.json();
            console.log("Usuário cadastrado:", data);

            console.log({ username, password });
            customAlert("Usuário cadastrado com sucesso!");

            window.navigateTo("/dashboard");
        } catch (error) {
            console.error("Erro:", error);
            customAlert("Falha ao cadastrar usuário." , error.message);
        }
    });
}

const backLink = document.getElementById("backToLogin");
if (backLink) {
    backLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/dashboard");
    });
}
