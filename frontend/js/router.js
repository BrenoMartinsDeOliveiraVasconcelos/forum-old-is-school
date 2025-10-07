document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");

  // ====== CARREGA HEADER ÚNICO ======
  async function loadHeader() {
    const headerContainer = document.getElementById("header-container");
    if (!headerContainer) return;

    const res = await fetch("/frontend/templates/header.html");
    if (!res.ok) {
      headerContainer.innerHTML = "<h2>Header não encontrado</h2>";
      return;
    }

    const html = await res.text();
    headerContainer.innerHTML = html;

    // Adiciona listener do link "Início"
    const homeLink = document.getElementById("homeLink");
    if (homeLink) {
      homeLink.addEventListener("click", (e) => {
        e.preventDefault();
        window.navigateTo("/dashboard");
      });
    }
  }

  // ====== CARREGA AS PÁGINAS ======
  async function loadView(view) {
    const res = await fetch(`/frontend/templates/${view}.html`);
    if (!res.ok) {
      app.innerHTML = `<h2>Página não encontrada</h2>`;
      return;
    }

    const html = await res.text();
    app.innerHTML = html;

    // ======= CARREGA CSS ESPECÍFICO DA PÁGINA =======
    const oldPageCss = document.getElementById("page-specific-css");
    if (oldPageCss) oldPageCss.remove();
    const pageCss = document.createElement("link");
    pageCss.rel = "stylesheet";
    pageCss.id = "page-specific-css";
    pageCss.href = `/frontend/assets/css/${view}.css`;
    pageCss.onerror = () => pageCss.remove();
    document.head.appendChild(pageCss);

    // === JS BASE (carrega em todas as páginas) ===
    const oldBaseScript = document.getElementById("base-js");
    if (!oldBaseScript) {
      const baseScript = document.createElement("script");
      baseScript.id = "base-js";
      baseScript.src = "/frontend/js/base.js";
      baseScript.type = "module";
      document.body.appendChild(baseScript);
    }

    // ====== CARREGA JS ESPECÍFICO DA PÁGINA ======
    const oldPageScript = document.getElementById("page-specific-js");
    if (oldPageScript) oldPageScript.remove();
    const pageScript = document.createElement("script");
    pageScript.id = "page-specific-js";
    pageScript.src = `/frontend/js/${view}.js`;
    pageScript.type = "module";
    pageScript.onerror = () => pageScript.remove();
    document.body.appendChild(pageScript);
  }

  // ====== DEFINE A PÁGINA INICIAL ======
  function router() {
    const hash = window.location.hash || "#/dashboard";
    if (hash === "#") loadView("dashboard");
    else if (hash === "#/dashboard") loadView("dashboard");
    else if (hash === "#/register") loadView("register");
    else app.innerHTML = "<h2>Página não encontrada</h2>";
  }

  // ====== AJUSTA A URL PARA QUE RECARREGUE A PAGINA ATUAL ======
  function navigateTo(path) {
    window.location.hash = "#" + path;
    if (path == '/') {
       window.location.hash = path;
    }
  }

  window.addEventListener("hashchange", router);
  window.addEventListener("popstate", router);

  loadHeader();
  router();

  window.navigateTo = navigateTo;
});
