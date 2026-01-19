import { API } from "./config.js";
import { tokens } from "../storage/tokens.js";

export async function request(url, options = {}, retry = true) {
    const headers = options.headers ? { ...options.headers } : {};
    if (tokens.access) headers.Authorization = `Bearer ${tokens.access}`;
    const res = await fetch(url, { ...options, headers });

    if (res.status === 401 && retry && tokens.refresh) {
        await refreshToken();
        return request(url, options, false);
    }

    return res;
}

async function refreshToken() {
    const res = await fetch(API.refresh, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: tokens.refresh })
    });

    if (!res.ok) throw new Error("Refresh failed");
    const data = await res.json();
    tokens.set({ access: data.access });
}
