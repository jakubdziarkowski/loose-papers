export const tokens = {
    get access() { return localStorage.getItem("access"); },
    get refresh() { return localStorage.getItem("refresh"); },
    set({ access, refresh }) {
        if (access) localStorage.setItem("access", access);
        if (refresh) localStorage.setItem("refresh", refresh);
    },
    clear() {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
    }
};
