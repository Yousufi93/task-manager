const API_URL = "http://127.0.0.1:8000";

const taskInput = document.getElementById("task-input");
const addBtn = document.getElementById("add-btn");
const taskList = document.getElementById("task-list");

async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        taskList.innerHTML = "<tr><td colspan='4' style='text-align:center;'>No tasks yet. Add one!</td></tr>";
        return;
    }

    tasks.forEach(task => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${task.id}</td>
            <td>${task.title}</td>
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

async function addTask() {
    const title = taskInput.value.trim();
    if (!title) return;

    try {
        await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title })
        });
        taskInput.value = "";
        loadTasks();
    } catch (error) {
        console.error("Error adding task:", error);
    }
}

async function markDone(taskId) {
    try {
        await fetch(`${API_URL}/tasks/${taskId}/done`, {
            method: "PATCH"
        });
        loadTasks();
    } catch (error) {
        console.error("Error marking task:", error);
    }
}

async function deleteTask(taskId) {
    try {
        await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE"
        });
        loadTasks();
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

addBtn.addEventListener("click", addTask);

taskInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") addTask();
});

loadTasks();