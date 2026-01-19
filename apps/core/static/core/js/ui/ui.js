export const ui = {
    showLogin() {
        document.getElementById("login").classList.remove("hidden");
        document.getElementById("app").classList.add("hidden");
    },
    showApp() {
        document.getElementById("login").classList.add("hidden");
        document.getElementById("app").classList.remove("hidden");
    },
    showLoginError(msg) {
        const el = document.getElementById("loginError");
        el.innerText = msg;
        el.classList.remove("d-none");
    },
    clearLoginError() {
        const el = document.getElementById("loginError");
        el.innerText = "";
        el.classList.add("d-none");
    }
};
