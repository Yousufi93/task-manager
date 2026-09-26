# 📝 Task Manager

A simple task manager built with **Python** — available both as a **command-line tool** and as a **REST API** built with **FastAPI**.

---

## ✨ Features

- ✅ Add new tasks
- 📋 Show all tasks with their status
- ✔️ Mark tasks as done
- 🗑️ Delete tasks
- 💾 Persistent storage with **SQLite**
- 🌐 Full **REST API** with automatic documentation (`/docs`)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Database | SQLite 3 |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| CLI | Custom menu in `mains.py` |
| Version Control | Git + GitHub |

---

## 📂 Project Structure

```
task-manager/
├── api.py              # FastAPI application (REST API)
├── database.py         # Database layer (SQLite)
├── task_manager.py     # CLI helper functions
├── mains.py            # CLI entry point (menu)
├── requirements.txt    # Dependencies
├── tasks.db            # SQLite database (auto-generated)
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Yousufi93/task-manager.git
cd task-manager
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Option A: Command-Line Interface (CLI)

Run the interactive menu:

```bash
python mains.py
```

You will see:

```
1. Add Task
2. Show Tasks
3. Mark Task as Done
4. Delete Task
5. Exit
```

### Option B: REST API

Start the API server:

```bash
uvicorn api:app --reload
```

Then open in your browser:

- **API root:** http://127.0.0.1:8000
- **Interactive docs (Swagger UI):** http://127.0.0.1:8000/docs

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks` | List all tasks |
| `POST` | `/tasks` | Create a new task |
| `PATCH` | `/tasks/{id}/done` | Mark a task as done |
| `DELETE` | `/tasks/{id}` | Delete a task |

### Example requests

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

**Mark task 1 as done:**
```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1/done
```

**Delete task 1:**
```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

---

## 🎓 What I Learned

This is my first full Python project. Through building it, I learned:

- Writing **functions**, **loops**, and **modules** in Python
- Working with **SQLite** databases (CRUD operations)
- Building a **REST API** with **FastAPI**
- Using **Pydantic** for data validation
- Handling **HTTP methods** (GET, POST, PATCH, DELETE) and **status codes** (200, 404, 422)
- Using **Git & GitHub** for version control

---

## 📌 Future Improvements

- [ ] Add user authentication
- [ ] Add task priorities and due dates
- [ ] Build a web UI (frontend)
- [ ] Migrate to PostgreSQL for production

---

## 📄 License

This project is for learning purposes. Feel free to use it.