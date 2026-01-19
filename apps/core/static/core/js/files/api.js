import { API } from "../api/config.js";
import { request } from "../api/client.js";

export async function listFiles() {
    const res = await request(API.files);
    if (!res.ok) throw new Error("Failed to load files");
    return res.json();
}

export async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", file.name);
    const res = await request(API.files, { method: "POST", body: formData });
    if (!res.ok) throw new Error("Upload failed");
}

export async function deleteFile(id) {
    const res = await request(`${API.files}${id}/`, { method: "DELETE" });
    if (!res.ok) throw new Error("Delete failed");
}

export async function downloadFile(id) {
    const res = await request(`${API.files}${id}/download/`);
    if (!res.ok) throw new Error("Download failed");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    const disposition = res.headers.get("Content-Disposition");
    let filename = "file";
    if (disposition && disposition.includes("filename=")) {
        filename = disposition.split("filename=")[1].replace(/"/g, "");
    }
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
}
