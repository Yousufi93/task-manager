const API_URL = "http://127.0.0.1:8000";

const taskInput = document.getElementById("task-input");
const addBtn = document.getElementById("add-btn");
const taskList = document.getElementById("task-list");
const prioritySelect = document.getElementById("priority-select");

let allTasks = [];
let currentFilter = "all";
let sortByPriority = false;
let searchQuery = "";
let statusFilter = "all";

// ==================== توابع احراز هویت ====================

function getAuthHeaders() {
    const token = localStorage.getItem("token");
    if (!token) {
        return { "Content-Type": "application/json" };
    }
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

function showLoginScreen() {
    document.getElementById("login-screen").style.display = "flex";
    document.getElementById("app-screen").style.display = "none";
}

function showAppScreen() {
    document.getElementById("login-screen").style.display = "none";
    document.getElementById("app-screen").style.display = "block";
    loadTasks();
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    showLoginScreen();
}

async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const errorEl = document.getElementById("login-error");
    errorEl.textContent = "";

    try {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData
        });

        if (!response.ok) {
            errorEl.textContent = "Invalid username or password";
            return;
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", username);
        showAppScreen();
    } catch (error) {
        console.error("Login error:", error);
        errorEl.textContent = "Connection error. Please try again.";
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    const errorEl = document.getElementById("register-error");
    errorEl.textContent = "";

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const data = await response.json();
            errorEl.textContent = data.detail || "Registration failed";
            return;
        }

        document.getElementById("tab-login").click();
        document.getElementById("login-username").value = username;
        document.getElementById("login-password").focus();
    } catch (error) {
        console.error("Register error:", error);
        errorEl.textContent = "Connection error. Please try again.";
    }
}

// ==================== تسک‌ها ====================

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`, {
            headers: getAuthHeaders()
        });
        if (response.status === 401) {
            logout();
            return;
        }
        allTasks = await response.json();
        applyFilter();
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = "";
    if (tasks.length === 0) {
        taskList.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No tasks found.</td></tr>";
        return;
    }
    tasks.forEach(task => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${task.id}</td>
            <td>${task.title}</td>
            <td>
                <span class="priority ${task.priority || 'medium'}">
                    ${task.priority || 'medium'}
                </span>
            </td>
            <td>
                <span class="status ${task.done ? 'done' : 'pending'}">
                    ${task.done ? 'Done' : 'Pending'}
                </span>
            </td>
            <td>
                <button class="btn-done" onclick="markDone(${task.id})">✓</button>
                <button class="btn-delete" onclick="deleteTask(${task.id})">✗</button>
            </td>
        `;
        taskList.appendChild(row);
    });
}

function applyFilter() {
    let filtered;
    if (currentFilter === "all") {
        filtered = [...allTasks];
    } else {
        filtered = allTasks.filter(task => task.priority === currentFilter);
    }
    if (statusFilter === "done") {
        filtered = filtered.filter(task => task.done === true);
    } else if (statusFilter === "pending") {
        filtered = filtered.filter(task => task.done === false);
    }
    if (searchQuery.trim() !== "") {
        const query = searchQuery.toLowerCase();
        filtered = filtered.filter(task =>
            task.title.toLowerCase().includes(query)
        );
    }
    if (sortByPriority) {
        const order = { high: 1, medium: 2, low: 3 };
        filtered.sort((a, b) => order[a.priority] - order[b.priority]);
    }
    renderTasks(filtered);
}

function setupFilters() {
    const buttons = document.querySelectorAll(".filter-btn");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            currentFilter = btn.dataset.priority;
            applyFilter();
        });
    });
}

function setupStatusFilters() {
    const buttons = document.querySelectorAll(".status-filter-btn");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            statusFilter = btn.dataset.status;
            applyFilter();
        });
    });
}

function setupSort() {
    const sortBtn = document.getElementById("sort-btn");
    sortBtn.addEventListener("click", () => {
        sortByPriority = !sortByPriority;
        sortBtn.classList.toggle("active", sortByPriority);
        applyFilter();
    });
}

function setupSearch() {
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value;
        applyFilter();
    });
}

async function addTask() {
    const title = taskInput.value.trim();
    if (!title) return;
    if (addBtn.disabled) return;
    addBtn.disabled = true;
    addBtn.textContent = "Adding...";
    const priority = prioritySelect.value;
    try {
        await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({ title: title, priority: priority })
        });
        taskInput.value = "";
        loadTasks();
    } catch (error) {
        console.error("Error adding task:", error);
    } finally {
        addBtn.disabled = false;
        addBtn.textContent = "Add Task";
    }
}

async function markDone(taskId) {
    try {
        await fetch(`${API_URL}/tasks/${taskId}/done`, {
            method: "PATCH",
            headers: getAuthHeaders()
        });
        loadTasks();
    } catch (error) {
        console.error("Error marking task:", error);
    }
}

async function deleteTask(taskId) {
    try {
        await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE",
            headers: getAuthHeaders()
        });
        loadTasks();
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

async function clearAllTasks() {
    const confirmed = confirm("Are you sure you want to delete ALL tasks?\n\nThis cannot be undone.");
    if (!confirmed) return;
    try {
        await fetch(`${API_URL}/tasks`, {
            method: "DELETE",
            headers: getAuthHeaders()
        });
        loadTasks();
    } catch (error) {
        console.error("Error clearing tasks:", error);
    }
}

// ==================== Setup Listeners (فقط یک بار) ====================

document.addEventListener("DOMContentLoaded", () => {
    // تسک‌ها
    addBtn.addEventListener("click", addTask);
    taskInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") addTask();
    });
    document.getElementById("clear-btn").addEventListener("click", clearAllTasks);

    setupFilters();
    setupStatusFilters();
    setupSort();
    setupSearch();

    // Login / Register
    document.getElementById("login-form").addEventListener("submit", handleLogin);
    document.getElementById("register-form").addEventListener("submit", handleRegister);

    document.getElementById("tab-login").addEventListener("click", () => {
        document.getElementById("tab-login").classList.add("active");
        document.getElementById("tab-register").classList.remove("active");
        document.getElementById("login-form").style.display = "block";
        document.getElementById("register-form").style.display = "none";
    });

    document.getElementById("tab-register").addEventListener("click", () => {
        document.getElementById("tab-register").classList.add("active");
        document.getElementById("tab-login").classList.remove("active");
        document.getElementById("register-form").style.display = "block";
        document.getElementById("login-form").style.display = "none";
    });

    // بررسی اولیه
    if (localStorage.getItem("token")) {
        showAppScreen();
    } else {
        showLoginScreen();
    }
});