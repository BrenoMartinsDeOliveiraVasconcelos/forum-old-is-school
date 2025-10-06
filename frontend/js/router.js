document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");

  // Carrega uma view do templates
  async function loadView(view) {
    const res = await fetch(`frontend/templates/${view}.html`);
    if (!res.ok) {
      app.innerHTML = `<h2>Página não encontrada</h2>`;
      return;
    }
    const html = await res.text();
    app.innerHTML = html;

    // Se for dashboard, adiciona logout
    if (view === "dashboard") {
      const btn = document.getElementById("logoutBtn");
      if (btn) btn.addEventListener("click", () => navigateTo("/login"));
    }

    // Se for login, intercepta submit
    if (view === "login") {
      const form = document.getElementById("loginForm");
      if (form) {
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          // Aqui você pode fazer fetch POST para validar usuário
          navigateTo("/dashboard");
        });
      }
    }
  }
function router() {
  const hash = window.location.hash || "#/login";
  if(hash === "#/login") loadView("login");
  else if(hash === "#/dashboard") loadView("dashboard");
  else app.innerHTML = "<h2>Página não encontrada</h2>";
}

window.addEventListener("hashchange", router);
window.addEventListener("DOMContentLoaded", router);

function navigateTo(hash) {
  window.location.hash = hash;
}

  // Quando navega com os botões do browser
  window.addEventListener("popstate", router);

  // Inicial
  router();

  // Expondo navigateTo globalmente (opcional)
  window.navigateTo = navigateTo;
});
