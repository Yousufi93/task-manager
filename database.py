import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("tasks.db")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER, priority TEXT DEFAULT 'medium', owner TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, priority='medium', owner=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done, priority, owner) VALUES (?, ?, ?, ?)", (title, 0, priority, owner))
    conn.commit()
    conn.close()

def get_all_tasks():
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("SELECT * FROM tasks")
     rows = cursor.fetchall()
     conn.close()
     return rows


def mark_done(task_id):
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("UPDATE tasks SET done =1 WHERE id = ?", (task_id,))
     conn.commit()
     conn.close()


def delete_task(task_id):
     conn = get_connection()
     cursor = conn.cursor()
     cursor .execute("DELETE FROM tasks WHERE id = ?", (task_id,))
     conn.commit()
     conn.close()
     reset_ids()



def reset_ids():
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT title, done, priority FROM tasks ORDER BY id")
        tasks = cursor.fetchall()
        
        cursor.execute("DROP TABLE IF EXISTS tasks")
        
        cursor.execute(""" 
            CREATE TABLE tasks ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT, 
                done INTEGER,
                priority TEXT DEFAULT 'medium'
            )
        """)
        
        for task in tasks:
            cursor.execute(
                "INSERT INTO tasks (title, done, priority) VALUES (?, ?, ?)",
                task
            )
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Error in reset_ids: {e}")
        raise
    finally:
        conn.close()


def clear_all_tasks():
     conn = get_connection()
     cursor = conn.sursor()
     try:
          cursor.execute("DELETE FROM tasks")
          cursor.execute("DELETE FROM sqlite_sequence WHERE name='tasks'")
          conn.commit()
     except Exception as e:
          conn.rollback()
          print(f"Error in clear_all_tasks: {e}")
          raise
     finally:
          conn.close()


def create_users_table():
     conn = get_connection()
     cursor = conn.cursor()
     cursor.execute("""
        CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT)
        """)
     conn.commit()
     conn.close()


def create_user(username, password_hash):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, password_hash, created_at)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
        create_table()
        create_users_table()
        print(" Tables created successfully.")
       


