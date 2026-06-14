from task import Task
from stack import Stack
from queue_tasks import Queue
from bst import BST
from datetime import datetime


def parse_date(date_str):
    """парсит дату из строки формата дд.мм.гггг"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        return None


def print_menu():
    print("\n=== Система управления задачами ===")
    print("1. Добавить задачу")
    print("2. Удалить задачу")
    print("3. Изменить приоритет задачи")
    print("4. Показать все задачи")
    print("5. Отменить последнее действие")
    print("6. Добавить задачу в очередь на исполнение")
    print("7. Взять задачу из очереди")
    print("8. Показать задачи по дедлайну (дерево)")
    print("9. Найти задачу с ближайшим дедлайном")
    print("10. Найти задачу с самым поздним дедлайном")
    print("0. Выйти")


def find_task_by_name(tasks, name):
    """линейный поиск задачи по названию"""
    for task in tasks:
        if task.name == name:
            return task
    return None


def main():
    tasks = []
    stack = Stack()
    queue = Queue()
    tree = BST()

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            name = input("Название задачи: ").strip()
            if not name:
                print("Название не может быть пустым.")
                continue
            if find_task_by_name(tasks, name):
                print("Задача с таким названием уже существует.")
                continue

            priority = input("Приоритет (1 - высокий, 2 - средний, 3 - низкий): ").strip()
            if priority not in ("1", "2", "3"):
                print("Приоритет должен быть 1, 2 или 3.")
                continue
            priority = int(priority)

            duration = input("Время выполнения (в часах): ").strip()
            try:
                duration = float(duration)
                if duration <= 0:
                    raise ValueError
            except ValueError:
                print("Введите корректное число часов.")
                continue

            deadline_str = input("Дедлайн (дд.мм.гггг): ").strip()
            deadline = parse_date(deadline_str)
            if deadline is None:
                print("Неверный формат даты. Используйте дд.мм.гггг.")
                continue

            task = Task(name, priority, duration, deadline)
            tasks.append(task)
            tree.insert(task)
            stack.push(("add", task))
            print("Задача добавлена.")

        elif choice == "2":
            if not tasks:
                print("Список задач пуст.")
                continue
            name = input("Название задачи для удаления: ").strip()
            task = find_task_by_name(tasks, name)
            if task is None:
                print("Задача не найдена.")
                continue
            tasks.remove(task)
            tree.rebuild(tasks)
            stack.push(("delete", task))
            print("Задача удалена.")

        elif choice == "3":
            if not tasks:
                print("Список задач пуст.")
                continue
            name = input("Название задачи: ").strip()
            task = find_task_by_name(tasks, name)
            if task is None:
                print("Задача не найдена.")
                continue
            new_priority = input("Новый приоритет (1 - высокий, 2 - средний, 3 - низкий): ").strip()
            if new_priority not in ("1", "2", "3"):
                print("Приоритет должен быть 1, 2 или 3.")
                continue
            old_priority = task.priority
            task.priority = int(new_priority)
            stack.push(("change", task, old_priority))
            print("Приоритет изменён.")

        elif choice == "4":
            if not tasks:
                print("Список задач пуст.")
                continue
            print("\n--- Список задач ---")
            priority_names = {1: "Высокий", 2: "Средний", 3: "Низкий"}
            for task in tasks:
                print(task.to_string(priority_names))

        elif choice == "5":
            if stack.is_empty():
                print("Нет действий для отмены.")
                continue
            action = stack.pop()

            if action[0] == "add":
                task = action[1]
                tasks.remove(task)
                tree.rebuild(tasks)
                print("Отменено добавление задачи:", task.name)

            elif action[0] == "delete":
                task = action[1]
                tasks.append(task)
                tree.rebuild(tasks)
                print("Отменено удаление задачи:", task.name)

            elif action[0] == "change":
                task = action[1]
                old_priority = action[2]
                task.priority = old_priority
                print("Отменено изменение приоритета задачи:", task.name)

        elif choice == "6":
            if not tasks:
                print("Список задач пуст.")
                continue
            name = input("Название задачи для добавления в очередь: ").strip()
            task = find_task_by_name(tasks, name)
            if task is None:
                print("Задача не найдена.")
                continue
            queue.enqueue(task)
            print("Задача добавлена в очередь.")

        elif choice == "7":
            if queue.is_empty():
                print("Очередь пуста.")
                continue
            task = queue.dequeue()
            priority_names = {1: "Высокий", 2: "Средний", 3: "Низкий"}
            print("Задача взята из очереди:")
            print(task.to_string(priority_names))

        elif choice == "8":
            if not tasks:
                print("Список задач пуст.")
                continue
            print("\n--- Задачи по дедлайну (от раннего к позднему) ---")
            result = []
            tree.inorder(tree.root, result)
            priority_names = {1: "Высокий", 2: "Средний", 3: "Низкий"}
            for task in result:
                print(task.to_string(priority_names))

        elif choice == "9":
            task = tree.find_min()
            if task is None:
                print("Дерево пусто.")
            else:
                priority_names = {1: "Высокий", 2: "Средний", 3: "Низкий"}
                print("Задача с ближайшим дедлайном:")
                print(task.to_string(priority_names))

        elif choice == "10":
            task = tree.find_max()
            if task is None:
                print("Дерево пусто.")
            else:
                priority_names = {1: "Высокий", 2: "Средний", 3: "Низкий"}
                print("Задача с самым поздним дедлайном:")
                print(task.to_string(priority_names))

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")


main()
