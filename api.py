from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import database
import auth 

app = FastAPI()
database.create_table()
database.create_users_table()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
    return username

# ----------------مدل های وردی ----------------

class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"

    # ------------------  endpoint -----------------
class UserCreate(BaseModel):
    username: str
    password: str


@app.get("/tasks")
def list_tasks(current_user: str = Depends(get_current_user)):
    rows = database.get_all_tasks()
    tasks = []
    for row in rows:
        task_id, title, done, priority, owner = row
        tasks.append({
            "id": task_id,
            "title": title,
            "done": bool(done),
            "priority": priority,
            "owner": owner
        })
    return tasks

@app.post("/tasks")
def create_task(payload: TaskCreate, current_user: str = Depends(get_current_user)):
    database.add_task(payload.title, payload.priority, current_user)
    return {
        "message": "Task created",
        "title": payload.title,
        "priority": payload.priority
    }

@app.patch("/tasks/{task_id}/done")
def mark_task_done(task_id: int, current_user: str = Depends(get_current_user)):
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]

    if task_id not in ids:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

    database.mark_done(task_id)
    return {
        "message": "Task marked as done",
        "id": task_id
    }


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int, current_user: str = Depends(get_current_user)):
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]

    if task_id not in ids:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )
    database.delete_task(task_id)
    return {
        "message": "Task deleted",
        "id": task_id
    }


@app.delete("/tasks")
def clear_tasks(current_user: str = Depends(get_current_user)):
    database.clear_all_tasks()
    return {
        "message": "All tasks cleared"
    }

@app.post("/register")
def register(user: UserCreate):

    existing = database.get_user_by_username(user.username)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    password_hash = auth.hash_password(user.password)
    

    success = database.create_user(user.username, password_hash)
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )
    
    return {
        "message": "User registered successfully",
        "username": user.username
    }



@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # پیدا کردن کاربر
    user = database.get_user_by_username(form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # بررسی پسورد
    # user ساختار: (id, username, password_hash, created_at)
    password_hash = user[2]
    
    if not auth.verify_password(form_data.password, password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    
    # ساخت توکن
    access_token = auth.create_access_token(form_data.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
