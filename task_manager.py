from storage import save_tasks

tasks = []


def add_task():
    task = input("Enter task title: ")
    tasks.append({"title": task, "done": False})
    save_tasks(tasks)
    print(f"Added: {task}")


def show_task():
    print("\\n1. Your tasks:")
    for t in tasks:
        status = "Done" if t["done"] else "Not Done"
        print(f"- {t['title']} [{status}]")


def mark_task_done():
    for i, t in enumerate(tasks, start=1):
        print(i, t["title"])
    num = int(input(" Which task number is done? "))
    if 1 <= num <= len(tasks):
        tasks[num -1]["done"] = True
        save_tasks(tasks)
        print("Marked as done.")
    else:
        print("Invalid task number. ")

def delete_task():
    for i, t in enumerate(tasks, start=1):
        print(i, t["title"])
    try:
        num = int(input("Which task number do you want to delete? "))
    except ValueError:
        print("Please enter a number.")
        return
    if 1 <= num <= len(tasks):
        removed = tasks.pop(num - 1)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}.")
    else:
        print("Invalid task number.")
