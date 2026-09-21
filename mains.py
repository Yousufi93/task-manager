from storage import load_tasks
import task_manager

task_manager.tasks = load_tasks()


while True:       
    print("\n1. Add Task\n2. Show Tasks\n3. Mark Task as Done\n4. Delete Task\n5. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        task_manager.add_task()

    elif choice == "2":
        task_manager.show_task()

    elif choice == "3":
       task_manager.mark_task_done()  
         
    elif choice == "4":
        task_manager.delete_task()

    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid choice, try again.")
        
        