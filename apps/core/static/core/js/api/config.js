const urlsEl = document.getElementById("urls");

export const API = {
    login: urlsEl.dataset.loginUrl,
    logout: urlsEl.dataset.logoutUrl,
    refresh: urlsEl.dataset.refreshUrl,
    me: urlsEl.dataset.meUrl,
    files: urlsEl.dataset.filesUrl
};
