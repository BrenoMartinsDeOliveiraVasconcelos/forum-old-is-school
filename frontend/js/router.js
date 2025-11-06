document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");

  async function loadComponent(containerId, url) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const res = await fetch(url);
    if (!res.ok) {
      container.innerHTML = `<h2>Componente não encontrado</h2>`;
      return;
    }

    container.innerHTML = await res.text();
  }

  // ====== CARREGA AS PÁGINAS ======
  async function loadView(view) {
    const mainCol = document.getElementById("main-col");
    if (!mainCol) return;

    const res = await fetch(`/frontend/templates/${view}.html`);
    if (!res.ok) {
      mainCol.innerHTML = `<h2>Página não encontrada</h2>`;
      return;
    }

    const html = await res.text();
    mainCol.innerHTML = html;
    document.dispatchEvent(new CustomEvent("viewLoaded", { detail: { view } }));

    // ======= CARREGA CSS ESPECÍFICO DA PÁGINA =======
    const oldPageCss = document.getElementById("page-specific-css");
    if (oldPageCss) oldPageCss.remove();
    const pageCss = document.createElement("link");
    pageCss.rel = "stylesheet";
    pageCss.id = "page-specific-css";
    pageCss.href = `/frontend/assets/css/${view}.css`;
    pageCss.onerror = () => pageCss.remove();
    document.head.appendChild(pageCss);

    // ====== JS BASE (carrega em todas as páginas) ======
    const oldBaseScript = document.getElementById("base-js");
    if (!oldBaseScript) {
      const baseScript = document.createElement("script");
      baseScript.id = "base-js";
      baseScript.src = "/frontend/js/base.js";
      baseScript.type = "module";
      document.body.appendChild(baseScript);
    }
    const oldBaseConfig = document.getElementById("config-js");
    if (!oldBaseConfig) {
      const baseConfig = document.createElement("script");
      baseConfig.id = "config-js";
      baseConfig.src = "/frontend/js/config.js";
      baseConfig.type = "module";
      document.body.appendChild(baseConfig);
    }
    const oldCKEditorScript = document.getElementById("ckeditor-js");
    if (!oldCKEditorScript) {
      const CKEditorScript = document.createElement("script");
      CKEditorScript.id = "ckeditor-js";
      CKEditorScript.src = "https://cdn.ckeditor.com/ckeditor5/47.1.0/ckeditor5.umd.js";
      CKEditorScript.type = "module";
      document.body.appendChild(CKEditorScript);
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
    else if (hash === "#/forum") loadView("forum");
    else if (hash === "#/novo_post") loadView("new_post");
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
  // ====== CARREGA OS COMPONENTES ======
  loadComponent("header-container", "frontend/templates/partial/header.html");
  loadComponent("sidebar-left-container", "frontend/templates/partial/sidebar-left.html");
  loadComponent("sidebar-right-container", "frontend/templates/partial/sidebar-right.html");
  router();

  window.navigateTo = navigateTo;
});
