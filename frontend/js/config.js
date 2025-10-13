export async function loadConfig() {
    try {
        const response = await fetch("/config.json");
        if (!response.ok) throw new Error("Erro ao carregar config.json");

        const config = await response.json();
        return config;
    } catch (err) {
        console.error("Falha ao carregar configuração:", err);
        return null;
    }
}
