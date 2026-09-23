import database


def add_task():
    task = input("Enter task title: ")
    database.add_task(task)
    print(f"Added: {task}")


def show_task():
    print("\n Your tasks:")
    rows = database.get_all_tasks()
    for row in rows:
        task_id, title, done = row
        status = "Done" if done == 1  else "Not Done"
        print(f"{task_id}. {title} [{status}]")


def mark_task_done():
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]
    for row in rows:
        task_id, title, done = row
        print(task_id, title)
    try:
        task_id= int(input("Which task number is done? "))
    except ValueError:
        print("Please enter a number. ")
        return
    
    if task_id in ids:
        database.mark_done(task_id)
        print("Marked as done.")
    else: 
        print("Invalid task number.")
   

def delete_task():
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]
    for row in rows:
        task_id, title, done = row
        print(task_id, title)
    try:
        task_id = int(input("Which task number do you want to delete? "))
    except ValueError:
        print("Please enter a number.")
        return
    if task_id in ids:
        database.delete_task(task_id)
        print("Deleted:")
    else:
        print("Invalid task number.")
   