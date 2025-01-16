import os
import json
from typing import List
from datetime import datetime, timedelta
from tabulate import tabulate

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        completed: bool = False,
        created_at: str = None,
        completed_at: str = None,
        deadline: str = None
    ):
        try:  # SCRUM-10: Перехват любых ошибок при инициализации
            self.title = title
            self.description = description
            self.completed = completed
            self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.completed_at = completed_at
            self.deadline = deadline
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при инициализации Task: {e}")  # SCRUM-10

    def mark_completed(self):
        try:  # SCRUM-10
            self.completed = True
            self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при завершении задачи: {e}")  # SCRUM-10

    def mark_incomplete(self):
        try:  # SCRUM-10
            self.completed = False
            self.completed_at = None
            self.deadline = None
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при изменении статуса задачи: {e}")  # SCRUM-10

    def set_deadline(self, deadline: str):
        if self.completed:
            print("Задача уже выполнена. Установка срока невозможна.")
            return False
        try:
            deadline_time = datetime.strptime(deadline, "%H:%M %d.%m.%Y")
            self.deadline = deadline_time.strftime("%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            print("Некорректный формат даты. Используйте формат 'ЧЧ:ММ ДД.ММ.ГГГГ'.")
            return False
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при установке срока: {e}")  # SCRUM-10
            return False

    def remaining_time(self):
        try:  # SCRUM-10
            if not self.deadline:
                return "[ ]"
            if self.completed:
                return "[ ]"
            deadline_time = datetime.strptime(self.deadline, "%Y-%m-%d %H:%M:%S")
            remaining = deadline_time - datetime.now()
            if remaining.total_seconds() > 0:
                days = remaining.days
                if days >= 1:
                    return f"Более {days} дней"
                else:
                    hours, remainder = divmod(remaining.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    return f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                return "[Срок истек]"
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при расчете оставшегося времени: {e}")  # SCRUM-10
            return "[Ошибка]"

    def to_dict(self, index: int):
        try:  # SCRUM-10
            return {
                "#": index,
                "Статус": "[X]" if self.completed else "[ ]",
                "Время": self.remaining_time(),
                "Название задачи": self.title,
                "Описание задачи": self.description,
                "Создано": self.created_at,
                "Завершено": self.completed_at if self.completed else ""
            }
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при преобразовании задачи в словарь: {e}")  # SCRUM-10
            return {}

class TaskManager:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.filename = f"{user_name.replace(' ', '_')}_tasks.json"
        self.last_saved = False
        try:  # SCRUM-10
            if os.path.exists(self.filename):
                self.load_from_file()
            else:
                self.tasks: List[Task] = []
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при инициализации TaskManager: {e}")  # SCRUM-10

    def add_task(self, title: str, description: str):
        try:  # SCRUM-10
            task = Task(title, description)
            self.tasks.append(task)
            self.last_saved = False
            print("Задача добавлена.")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при добавлении задачи: {e}")  # SCRUM-10

    def remove_task(self, index: int):
        try:  # SCRUM-10
            if not self.tasks:
                print("Список задач пуст. Удаление невозможно.")
                return

            if 0 <= index < len(self.tasks):
                removed_task = self.tasks.pop(index)
                self.last_saved = False
                print(f"Задача \"{removed_task.title}\" удалена.")
            else:
                print("Неверный индекс.")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при удалении задачи: {e}")  # SCRUM-10

    def view_tasks(self):
        try:  # SCRUM-10
            if not self.tasks:
                print("Список задач пуст.")
            else:
                tasks_data = [task.to_dict(i + 1) for i, task in enumerate(self.tasks)]
                print(tabulate(tasks_data, headers="keys", tablefmt="grid"))
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при просмотре задач: {e}")  # SCRUM-10

    def change_task_status(self, index: int):
        try:  # SCRUM-10
            if not self.tasks:
                print("Список задач пуст. Изменение статуса невозможно.")
                return

            if 0 <= index < len(self.tasks):
                task = self.tasks[index]
                if task.completed:
                    task.mark_incomplete()
                    print(f"Статус задачи \"{task.title}\" изменен на невыполненный.")
                else:
                    task.mark_completed()
                    print(f"Задача \"{task.title}\" отмечена как выполненная.")
                self.last_saved = False
            else:
                print("Неверный индекс.")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при изменении статуса задачи: {e}")  # SCRUM-10

    def set_task_deadline(self, index: int, deadline: str):
        try:  # SCRUM-10
            if not self.tasks:
                print("Список задач пуст. Установка срока невозможна.")
                return

            if 0 <= index < len(self.tasks):
                if not self.tasks[index].set_deadline(deadline):
                    return
                self.last_saved = False
                print(f"Для задачи \"{self.tasks[index].title}\" установлен срок выполнения.")
            else:
                print("Неверный индекс.")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка при установке срока задачи: {e}")  # SCRUM-10

    def save_to_file(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([task.__dict__ for task in self.tasks], file, ensure_ascii=False, indent=4)
            self.last_saved = True
            print(f"Список задач сохранен в файл \"{self.filename}\".")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка сохранения в файл: {e}")  # SCRUM-10

    def save_report(self):
        try:
            completed_tasks = [task.to_dict(i + 1) for i, task in enumerate(self.tasks) if task.completed]
            if not completed_tasks:
                print("Нет выполненных задач для сохранения в отчете.")
                return

            for task in completed_tasks:
                task.pop("Статус")
                task.pop("Время")

            for i, task in enumerate(completed_tasks, start=1):
                task["#"] = i

            report_filename = f"{self.user_name.replace(' ', '_')}_report_task_completed.txt"
            with open(report_filename, 'w', encoding='utf-8') as report_file:
                report_file.write(tabulate(completed_tasks, headers="keys", tablefmt="grid"))
            print(f"Отчет выполненных задач сохранен в файл \"{report_filename}\".")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка сохранения отчета: {e}")  # SCRUM-10

    def load_from_file(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**data) for data in tasks_data]
            self.last_saved = True
            print(f"Список задач загружен из файла \"{self.filename}\".")
        except FileNotFoundError:
            print(f"Файл \"{self.filename}\" не найден. Будет создан новый файл при сохранении.")
        except json.JSONDecodeError:
            print("Ошибка чтения данных из файла.")  # SCRUM-10
        except Exception as e:  # SCRUM-10
            print(f"Произошла ошибка при загрузке: {e}")  # SCRUM-10

class UserManager:
    def __init__(self):
        self.filename = "users.txt"
        self.users = self.load_users()

    def add_user(self, first_name: str, last_name: str):
        user_name = f"{first_name} {last_name}"
        if user_name in self.users:
            print(f"Пользователь {user_name} уже существует.")
        else:
            self.users.append(user_name)
            self.save_users()
            print(f"Пользователь {user_name} добавлен.")

    def remove_user(self, user_name: str):
        if user_name in self.users:
            self.users.remove(user_name)
            self.save_users()
            print(f"Пользователь {user_name} удален.")
        else:
            print("Такого пользователя не существует.")

    def list_users(self):
        if not self.users:
            print("Список пользователей пуст.")
        else:
            print("=" * 36)
            print("Список пользователей:")
            for i, user in enumerate(self.users, 1):
                print(f"{i}. {user}")
        print("=" * 36)

    def save_users(self):
        try:  # SCRUM-10
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write("\n".join(self.users))
            print("Список пользователей сохранен.")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка сохранения списка пользователей: {e}")  # SCRUM-10

    def load_users(self):
        if os.path.exists(self.filename):
            try:  # SCRUM-10
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return [line.strip() for line in file if line.strip()]
            except Exception as e:  # SCRUM-10
                print(f"Ошибка загрузки списка пользователей: {e}")  # SCRUM-10
        return []

    def save_report_all_users(self):
        try:  # SCRUM-10
            report_filename = "report.txt"
            with open(report_filename, 'w', encoding='utf-8') as report_file:
                for user_name in self.users:
                    task_manager = TaskManager(user_name)
                    completed_tasks = [t.to_dict(i + 1) for i, t in enumerate(task_manager.tasks) if t.completed]

                    if completed_tasks:
                        report_file.write(f"Отчет для пользователя: {user_name}\n")
                        for task in completed_tasks:
                            task.pop("Статус")
                            task.pop("Время")

                        for i, task in enumerate(completed_tasks, start=1):
                            task["#"] = i

                        report_file.write(tabulate(completed_tasks, headers="keys", tablefmt="grid"))
                        report_file.write("\n\n")
                    else:
                        report_file.write(f"Нет выполненных задач для пользователя {user_name}\n\n")
            print(f"Общий отчет о выполненных задачах всех пользователей сохранен в файл \"{report_filename}\".")
        except Exception as e:  # SCRUM-10
            print(f"Ошибка сохранения общего отчета: {e}")  # SCRUM-10

def validate_name(prompt):
    while True:
        try:  # SCRUM-10
            name = input(prompt).strip()
        except EOFError:  # SCRUM-10
            print("Ввод прерван. Попробуйте снова.")  # SCRUM-10
            continue
        if name.isalpha() and name.isascii():
            return name
        print("Введите корректное имя (только латинские буквы).")

def main():
    user_manager = UserManager()

    while True:
        print("\n===========Главное меню:============")
        print("1. Добавить пользователя")
        print("2. Удалить пользователя")
        print("3. Просмотреть список пользователей")
        print("4. Менеджер задач пользователя")
        print("5. Отчет о работе всех пользователей")
        print("0. Завершение программы")

        choice = input("Выберите действие: ").strip().lower()

        if choice == "1":
            first_name = validate_name("Введите имя пользователя: ")
            last_name = validate_name("Введите фамилию пользователя: ")
            user_manager.add_user(first_name, last_name)

        elif choice == "2":
            user_manager.list_users()
            try:
                user_index = int(input("Введите номер пользователя для удаления: ").strip()) - 1
                if 0 <= user_index < len(user_manager.users):
                    user_name = user_manager.users[user_index]
                    user_manager.remove_user(user_name)
                else:
                    print("Неверный номер пользователя.")
            except ValueError:  # SCRUM-10
                print("Введите корректный номер пользователя для удаления.")  # SCRUM-10

        elif choice == "3":
            user_manager.list_users()

        elif choice == "4":
            user_manager.list_users()
            try:  # SCRUM-10
                user_index = int(input("Выберите номер пользователя для управления задачами: ").strip()) - 1
                if 0 <= user_index < len(user_manager.users):
                    user_name = user_manager.users[user_index]
                    task_manager = TaskManager(user_name)
                    while True:
                        print(f"\nМеню задач для пользователя: {user_name}")
                        print("1. Просмотреть список задач")
                        print("2. Добавить задачу")
                        print("3. Удалить задачу")
                        print("4. Сохранить задачи в файл")
                        print("5. Изменить статус задачи")
                        print("6. Установить срок выполнения задачи")
                        print("7. Сохранить отчет выполненных задач")
                        print("0. Вернуться к списку пользователей")

                        task_choice = input("Выберите действие: ").strip()

                        if task_choice == "1":
                            task_manager.view_tasks()

                        elif task_choice == "2":
                            title = input("Введите название задачи: ").strip()
                            description = input("Введите описание задачи: ").strip()
                            task_manager.add_task(title, description)

                        elif task_choice == "3":
                            task_manager.view_tasks()
                            try:  # SCRUM-10
                                index = int(input("Введите номер задачи для удаления: ").strip()) - 1
                                task_manager.remove_task(index)
                            except ValueError:  # SCRUM-10
                                print("Введите корректный номер задачи для удаления.")  # SCRUM-10

                        elif task_choice == "4":
                            task_manager.save_to_file()

                        elif task_choice == "5":
                            task_manager.view_tasks()
                            try:  # SCRUM-10
                                index = int(input("Введите номер задачи для изменения статуса: ").strip()) - 1
                                task_manager.change_task_status(index)
                            except ValueError:  # SCRUM-10
                                print("Введите корректный номер задачи для изменения статуса.")  # SCRUM-10

                        elif task_choice == "6":
                            task_manager.view_tasks()
                            try:  # SCRUM-10
                                index = int(input("Введите номер задачи для установки срока выполнения: ").strip()) - 1
                                if task_manager.tasks[index].completed:
                                    print("Задача уже выполнена. Установка срока невозможна.")
                                    continue
                                deadline = input("Введите срок выполнения (формат ЧЧ:ММ ДД.ММ.ГГГГ): ").strip()
                                task_manager.set_task_deadline(index, deadline)
                            except ValueError:
                                print("Введите корректные данные о задаче.")  # SCRUM-10
                            except IndexError:
                                print("Неверный номер задачи.")  # SCRUM-10
                            except Exception as e:
                                print(f"Произошла непредвиденная ошибка: {e}")  # SCRUM-10

                        elif task_choice == "7":
                            task_manager.save_report()

                        elif task_choice == "0":
                            if not task_manager.last_saved:
                                while True:
                                    save_choice = input(
                                        "Сохранить изменения для текущего пользователя? (Yes (Y)/No (N)): "
                                    ).strip().lower()
                                    if save_choice in ("y", "yes"):
                                        task_manager.save_to_file()
                                        break
                                    elif save_choice in ("n", "no"):
                                        break
                                    else:
                                        print("Неверный выбор. Пожалуйста, введите Yes (Y) или No (N).")
                            break

                        else:
                            print("Неверный выбор, попробуйте снова.")
                else:
                    print("Неверный номер пользователя.")
            except ValueError:  # SCRUM-10
                print("Введите корректный номер пользователя.")  # SCRUM-10

        elif choice == "5":
            user_manager.save_report_all_users()

        elif choice == "0":
            print("Завершение программы. До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
