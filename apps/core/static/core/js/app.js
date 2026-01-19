import { tokens } from "./storage/tokens.js";
import { ui } from "./ui/ui.js";
import * as auth from "./auth/api.js";
import * as filesApi from "./files/api.js";
import {downloadFile} from "./files/api.js";

// --- DOM elements ---
const fileInput = document.getElementById("fileInput");
const uploadArea = document.getElementById("uploadArea");
const uploadBtn = document.getElementById("uploadBtn");
const selectedFilesArea = document.getElementById("selectedFilesArea");
const selectedFilesList = selectedFilesArea.querySelector(".selected-files-list");
const fileListEl = document.getElementById("fileList");

// --- state ---
let selectedFiles = [];

// --- helpers ---
function renderSelectedFiles() {
    if (!selectedFiles.length) {
        uploadArea.classList.remove("d-none");
        selectedFilesArea.classList.add("d-none");
        return;
    }
    uploadArea.classList.add("d-none");
    selectedFilesArea.classList.remove("d-none");
    selectedFilesList.innerHTML = "";
    selectedFiles.forEach((file, idx) => {
        const el = document.createElement("div");
        el.className = "selected-file-item d-flex justify-content-between align-items-center mb-1";
        el.innerHTML = `<span>${file.name}</span><button data-idx="${idx}" class="btn btn-sm btn-outline-danger">✕</button>`;
        el.querySelector("button").onclick = () => {
            selectedFiles.splice(idx, 1);
            syncFileInput();
            renderSelectedFiles();
        };
        selectedFilesList.appendChild(el);
    });
}

function syncFileInput() {
    const dt = new DataTransfer();
    selectedFiles.forEach(f => dt.items.add(f));
    fileInput.files = dt.files;
}

function renderFiles(files) {
    fileListEl.innerHTML = "";
    if (!files.length) {
        fileListEl.innerHTML = `<tr><td colspan="2" class="text-center text-muted">No files uploaded</td></tr>`;
        return;
    }
    files.forEach(f => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${f.name}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-primary">Download</button>
                <button class="btn btn-sm btn-outline-danger">Delete</button>
            </td>`;
        tr.querySelector(".btn-outline-primary").onclick = async () => {
            await filesApi.downloadFile(f.id);
        };
        tr.querySelector(".btn-outline-danger").onclick = async () => {
            await filesApi.deleteFile(f.id);
            await loadApp();
        };
        fileListEl.appendChild(tr);
    });
}

// --- main functions ---
async function loadApp() {
    const me = await auth.getMe();
    document.getElementById("me").innerText = JSON.stringify(me, null, 2);
    const files = await filesApi.listFiles();
    renderFiles(files);
}

// --- event listeners ---
uploadArea.addEventListener("click", () => fileInput.click());

uploadArea.addEventListener("dragover", e => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", e => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", e => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    selectedFiles = Array.from(e.dataTransfer.files);
    syncFileInput();
    renderSelectedFiles();
});

fileInput.addEventListener("change", () => {
    selectedFiles = Array.from(fileInput.files);
    renderSelectedFiles();
});

uploadBtn.onclick = async () => {
    if (!selectedFiles.length) return;
    for (const file of selectedFiles) await filesApi.uploadFile(file);
    selectedFiles = [];
    syncFileInput();
    renderSelectedFiles();
    await loadApp();
};

// --- login / logout ---
document.getElementById("loginForm").onsubmit = async e => {
    e.preventDefault();
    ui.clearLoginError();
    try {
        await auth.login(
            document.getElementById("email").value,
            document.getElementById("password").value
        );
        ui.showApp();
        await loadApp();
    } catch (err) {
        ui.showLoginError(err.message || "Login failed");
    }
};

document.getElementById("logoutBtn").onclick = async () => {
    await auth.logout();
    ui.showLogin();
};

// --- initial app state ---
document.addEventListener("DOMContentLoaded", () => {
    if (tokens.access) {
        ui.showApp();
        loadApp();
    } else {
        ui.showLogin();
    }
});
