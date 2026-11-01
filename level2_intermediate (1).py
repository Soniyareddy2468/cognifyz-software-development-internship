"""
Cognifyz Software Development Internship - Level 2: Intermediate
Task 3: Console CRUD application for a list of tasks (in-memory list)
Task 4: Temperature converter (Fahrenheit <-> Celsius)
"""


# ---------------------------------------------------------------- Task 3
class Task:
    def __init__(self, task_id, title, description="", status="Pending"):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status

    def __str__(self):
        return f"[{self.task_id}] {self.title} | {self.status} | {self.description or '-'}"


class TaskManager:
    STATUSES = ("Pending", "In Progress", "Done")

    def __init__(self):
        self.tasks = []
        self._next_id = 1

    # Create
    def create(self, title, description=""):
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        task = Task(self._next_id, title.strip(), description.strip())
        self.tasks.append(task)
        self._next_id += 1
        return task

    # Read
    def read_all(self):
        return list(self.tasks)

    def find(self, task_id):
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        return None

    # Update
    def update(self, task_id, title=None, description=None, status=None):
        task = self.find(task_id)
        if task is None:
            return False
        if title:
            task.title = title.strip()
        if description is not None and description != "":
            task.description = description.strip()
        if status:
            task.status = status
        return True

    # Delete
    def delete(self, task_id):
        task = self.find(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True


def read_int(prompt):
    raw = input(prompt).strip()
    return int(raw) if raw.isdigit() else None


def crud_app():
    manager = TaskManager()
    while True:
        print("\n--- TASK MANAGER ---")
        print("1) Add task\n2) View tasks\n3) Update task\n4) Delete task\n0) Back")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ")
            desc = input("Description (optional): ")
            try:
                t = manager.create(title, desc)
                print(f"Added: {t}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            tasks = manager.read_all()
            if not tasks:
                print("No tasks yet.")
            for t in tasks:
                print(t)

        elif choice == "3":
            tid = read_int("Task ID to update: ")
            if tid is None or manager.find(tid) is None:
                print("Task not found.")
                continue
            title = input("New title (blank to keep): ")
            desc = input("New description (blank to keep): ")
            print("Status: 1) Pending  2) In Progress  3) Done  (blank to keep)")
            s = input("Choose: ").strip()
            status = TaskManager.STATUSES[int(s) - 1] if s in ("1", "2", "3") else None
            manager.update(tid, title, desc, status)
            print("Updated.")

        elif choice == "4":
            tid = read_int("Task ID to delete: ")
            if tid is not None and manager.delete(tid):
                print("Deleted.")
            else:
                print("Task not found.")

        elif choice == "0":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------------------- Task 4
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def temperature_converter():
    while True:
        print("\n--- TEMPERATURE CONVERTER ---")
        print("1) Celsius -> Fahrenheit\n2) Fahrenheit -> Celsius\n0) Back")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        if choice not in ("1", "2"):
            print("Invalid option.")
            continue
        raw = input("Enter temperature: ").strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if choice == "1":
            print(f"{value:.2f} °C = {celsius_to_fahrenheit(value):.2f} °F")
        else:
            print(f"{value:.2f} °F = {fahrenheit_to_celsius(value):.2f} °C")


# ---------------------------------------------------------------- Menu
def main():
    while True:
        print("\n--- LEVEL 2 MENU ---")
        print("1) Task manager CRUD (Task 3)")
        print("2) Temperature converter (Task 4)")
        print("0) Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            crud_app()
        elif choice == "2":
            temperature_converter()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
