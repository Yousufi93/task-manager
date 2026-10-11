import sqlite3

def get_connection():
    return sqlite3.connect("tasks.db")


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done INTEGER, priority TEXT DEFAULT 'medium'
        )
    """)
    conn.commit()
    conn.close()

def add_task(title, priority='medium'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done, priority) VALUES (?, ?, ?)", (title, 0, priority))
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
    """id های تسک‌ها را از ۱ به‌ترتیب بازسازی می‌کند."""
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

if __name__ == "__main__":
        create_table()
        print("‌Before:", get_all_tasks())
        mark_done(1)
        print("After mark done:", get_all_tasks())
        delete_task(1)
        print("After delete:", get_all_tasks())
        

