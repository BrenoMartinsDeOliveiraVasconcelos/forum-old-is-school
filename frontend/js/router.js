document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");

  // ====== CARREGA AS PÁGINAS ======
  async function loadView(view) {
    const res = await fetch(`frontend/templates/${view}.html`);
    console.log(res);

    if (!res.ok) {
      app.innerHTML = `<h2>Página não encontrada</h2>`;
      return;
    }
    const html = await res.text();
    app.innerHTML = html;


    // ====== CARREGA O CSS ESPECÍFICO POR PAGINA ======
    const oldPageCss = document.getElementById("page-specific-css");
    if (oldPageCss) oldPageCss.remove();

    const pageCss = document.createElement("link");
    pageCss.rel = "stylesheet";
    pageCss.id = "page-specific-css";
    pageCss.href = `/frontend/assets/css/${view}.css`;

    pageCss.onerror = () => pageCss.remove();

    document.head.appendChild(pageCss);


    // ====== FAZ O LOGIN E CHAMA A DASHBOARD ======
    if (view === "login") {
      const form = document.getElementById("loginForm");
      if (form) {
        form.addEventListener("submit", (e) => {
          e.preventDefault();
          sessionStorage.setItem('auth', '1'); // mock auth
          navigateTo("/dashboard");
        });
      }
    }

    // ====== FAZ O LOGIN NO SIDEBAR ======
    const btnLoginSidebar = document.getElementById("loginBtn");
    if (btnLoginSidebar) {
      btnLoginSidebar.addEventListener("click", () => {
        navigateTo("/login");
      });
    }
  }


  // ====== DEFINE A PÁGINA INICIAL ======
  function router() {
    const hash = window.location.hash || "#/dashboard";
    if (hash === "#/login") loadView("login");
    else if (hash === "#/dashboard") loadView("dashboard");
    else app.innerHTML = "<h2>Página não encontrada</h2>";
  }

  // ====== AJUSTA A URL PARA QUE RECARREGUE A PAGINA ATUAL ======
  function navigateTo(path) {
    window.location.hash = "#" + path;
  }

  window.addEventListener("hashchange", router);
  window.addEventListener("popstate", router);
  router();

  window.navigateTo = navigateTo;
});
