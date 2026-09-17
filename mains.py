import json

def save_tasks():
        with open("tasks.json", "w") as f:
                  json.dump(tasks, f)

try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except  FileNotFoundError:
    tasks = []


def add_task():
    task =input("Enter task title:")
    tasks.append({"title": task, "done": False})
    save_tasks()
    print(f"Added: {task}")

def show_tasks():
    print("\n1. Your tasks:")
    for t in tasks:
        status = "Done" if t["done"] else "Not Done"
        print(f"- {t['title']} [{status}]")
def mark_task_done():
    for i, t in enumerate(tasks, start=1):
            print(i, t["title"])
    num = int(input(" Which task number is done?"))
    if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            save_tasks()
            print("Marked as done.")
    else:
            print("Invalid task number.")
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
            save_tasks()
            print(f"Deleted: {removed['title']}.")
        else:
            print("Invalid task number.")


while True:       
    print("\n1. Add Task\n2. Show Tasks\n3. Mark Task as Done\n4. Delete Task\n5. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        show_tasks()

    elif choice == "3":
        mark_task_done()

    elif choice == "4":
        delete_task()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")
        
        