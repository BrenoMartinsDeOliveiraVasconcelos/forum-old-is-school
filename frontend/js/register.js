const form = document.getElementById("registerForm");

if (form) {
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("As senhas não conferem!");
            return;
        }

        if (!username || !email || !password) {
            alert("Preencha todos os campos!");
            return;
        }

        // Mock de cadastro
        console.log({ username, email, password });
        alert("Usuário cadastrado com sucesso!");

        window.navigateTo("/dashboard");
    });
}

const backLink = document.getElementById("backToLogin");
if (backLink) {
    backLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/dashboard");
    });
}
