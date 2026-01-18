/********* CONFIG & TOKENS *********/
const urlsEl = document.getElementById("urls");
const LOGIN_URL = urlsEl.dataset.loginUrl;
const ME_URL = urlsEl.dataset.meUrl;
const LOGOUT_URL = urlsEl.dataset.logoutUrl;
const REFRESH_URL = urlsEl.dataset.refreshUrl;

function getAccess() { return localStorage.getItem("access"); }
function getRefresh() { return localStorage.getItem("refresh"); }
function setTokens({ access, refresh }) {
    if (access) localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
}
function clearTokens() { localStorage.clear(); }

/********* API CALLS *********/
async function apiPost(url, body, useAccess = true) {
    const headers = { "Content-Type": "application/json" };
    if (useAccess && getAccess()) headers["Authorization"] = `Bearer ${getAccess()}`;
    return fetch(url, { method: "POST", headers, body: JSON.stringify(body) });
}

async function loginAPI(email, password) { return apiPost(LOGIN_URL, { email, password }, false); }
async function logoutAPI() { if(getRefresh()) await apiPost(LOGOUT_URL, { refresh: getRefresh() }, false).catch(e => console.error(e)); }
async function refreshToken() {
    if (!getRefresh()) throw new Error("No refresh token");
    const res = await apiPost(REFRESH_URL, { refresh: getRefresh() }, false);
    if (!res.ok) throw new Error("Refresh failed");
    const data = await res.json();
    setTokens({ access: data.access });
    return data.access;
}
async function loadMeAPI() {
    let res = await fetch(ME_URL, { headers: { "Authorization": `Bearer ${getAccess()}` } });
    if (res.status === 401 && getRefresh()) {
        try { await refreshToken(); res = await fetch(ME_URL, { headers: { "Authorization": `Bearer ${getAccess()}` } }); }
        catch { throw new Error("Session expired"); }
    }
    if (!res.ok) throw new Error("Failed to fetch /me/");
    return res.json();
}

/********* UI HANDLERS *********/
async function login(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    try {
        const res = await loginAPI(email, password);
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            document.getElementById("loginError").innerText = data.detail || "Login failed";
            loginError.style.display = "block";
            return;
        }
        const data = await res.json();
        setTokens(data);
        showApp();
    } catch (err) { document.getElementById("loginError").innerText = "Network error"; console.error(err); }
}

async function loadMe() {
    try {
        const data = await loadMeAPI();
        document.getElementById("me").innerText = JSON.stringify(data, null, 2);
    } catch { clearTokens(); showLogin(); }
}

async function logout() { await logoutAPI(); clearTokens(); showLogin(); }
function showApp() { document.getElementById("login").classList.add("hidden"); document.getElementById("app").classList.remove("hidden"); loadMe(); }
function showLogin() { document.getElementById("login").classList.remove("hidden"); document.getElementById("app").classList.add("hidden"); }

/********* INIT *********/
document.getElementById("loginForm").addEventListener("submit", login);
document.getElementById("logoutBtn").addEventListener("click", logout);
if (getAccess()) showApp();
