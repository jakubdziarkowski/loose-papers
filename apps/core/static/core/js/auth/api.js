import { API } from "../api/config.js";
import { tokens } from "../storage/tokens.js";
import { request } from "../api/client.js";

export async function login(email, password) {
    const res = await fetch(API.login, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    if (!res.ok) throw new Error("Invalid credentials");
    const data = await res.json();
    tokens.set(data);
}

export async function logout() {
    try {
        await fetch(API.logout, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: tokens.refresh })
        });
    } finally {
        tokens.clear();
    }
}

export async function getMe() {
    const res = await request(API.me);
    if (!res.ok) throw new Error("Unauthorized");
    return res.json();
}
