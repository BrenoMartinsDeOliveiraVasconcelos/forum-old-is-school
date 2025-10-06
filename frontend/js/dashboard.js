/* AJUSTE DINÂMICO DO CONTEUDO DO DASHBOARD */
function ajustarDashboard() {
    const header = document.querySelector('header.site-header');
    const dashboard = document.querySelector('.dashboard-wrapper');

    if (!header || !dashboard) return;

    const alturaHeader = header.getBoundingClientRect().height;

    // Condicional baseada na largura da tela
    const larguraTela = window.innerWidth;
    let extraPadding = 0;

    if (larguraTela <= 1365) {
        extraPadding = 50;
    } else if (larguraTela <= 1920) {
        extraPadding = 20;
    } else {
        extraPadding = 30; // para telas maiores, se quiser
    }

    dashboard.style.paddingTop = (alturaHeader + extraPadding) + 'px';
}

// Ajusta no load e resize
window.addEventListener('load', ajustarDashboard);
window.addEventListener('resize', ajustarDashboard);
