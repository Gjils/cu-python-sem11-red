import uuid
from datetime import datetime
import os
import json
import logging
import pandas as pd
import operator


class Note:
    def __init__(self, title, content, timestamp=None, id=None):
        if id is None:
            id = str(uuid.uuid4())
        if timestamp == None:
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def edit_note(self, new_title=None, new_content=None):
        if not new_title is None:
            self.title = new_title
        if not new_content is None:
            self.content = new_content

    def to_json(self):
        return dict(
            id=self.id, title=self.title, content=self.content, timestamp=self.timestamp
        )

    def __str__(self) -> str:
        return f"Заметка {self.title} с ID {self.id}\nСодержание: {self.content}\nДата создания: {self.timestamp}"

    @staticmethod
    def from_json(note_json):
        return Note(**note_json)


class Task:
    def __init__(self, title, description, priority, due_date, id=None, done=None):
        if id is None:
            id = str(uuid.uuid4())
        if done == None:
            done = False
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def edit_note(
        self, new_title=None, new_description=None, new_priority=None, new_due_date=None
    ):
        if not new_title is None:
            self.title = new_title
        if not new_description is None:
            self.description = new_description
        if not new_priority is None:
            self.priority = new_priority
        if not new_due_date is None:
            self.due_date = new_due_date

    def toggle_done(self):
        self.done = not self.done

    def to_json(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            priority=self.priority,
            due_date=self.due_date,
        )

    def __str__(self) -> str:
        return f"Задача {self.title} с ID {self.id}\nCтатус: {self.done}\nПриоритет: {self.priority}\nДедлайн: {self.due_date}"

    @staticmethod
    def from_json(task_json):
        return Task(**task_json)


class Contact:
    def __init__(self, name, phone, email, id=None):
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

    def edit_contact(self, new_name=None, new_phone=None, new_email=None):
        if new_name is not None:
            self.name = new_name
        if new_phone is not None:
            self.phone = new_phone
        if new_email is not None:
            self.email = new_email

    def to_json(self):
        return dict(id=self.id, name=self.name, phone=self.phone, email=self.email)

    def __str__(self):
        return f"Контакт: {self.name} ({self.phone}, {self.email})"

    @staticmethod
    def from_json(contact_json):
        return Contact(**contact_json)


class FinanceRecord:
    def __init__(self, amount, category, date, description, id=None):
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def edit_record(
        self, new_amount=None, new_category=None, new_date=None, new_description=None
    ):
        if new_amount is not None:
            self.amount = new_amount
        if new_category is not None:
            self.category = new_category
        if new_date is not None:
            self.date = new_date
        if new_description is not None:
            self.description = new_description

    def to_json(self):
        return dict(
            id=self.id,
            amount=self.amount,
            category=self.category,
            date=self.date,
            description=self.description,
        )

    def __str__(self):
        return f"Запись: {self.amount} руб. ({self.category}) на {self.date} — {self.description}"

    @staticmethod
    def from_json(record_json):
        return FinanceRecord(**record_json)


class NoteManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.init_notes()

    def init_notes(self) -> None:
        if not os.path.isfile(self.filename):
            logging.warning(f"Файл {self.filename} не найден")
            with open(self.filename, "w") as file:
                file.write("{}")
                logging.info(f"Файл {self.filename} создан")
            self.notes = {}

        with open(self.filename, "r+") as file:
            try:
                notes = json.loads(file.read())
                logging.info(f"Файл {self.filename} найден и является валидным JSON")
                self.notes = notes
            except:
                logging.warning(f"Файл {self.filename} найден, но поврежден")
                file.seek(0)
                file.truncate(0)
                file.write("{}")
                logging.info(f"Файл {self.filename} перезаписан")
                self.notes = {}

    def save_to_file(self) -> None:
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.notes))

    def create_note(self, note: Note) -> None:
        self.notes[note.id] = note.to_json()
        self.save_to_file()
        logging.info(f"Заметка с ID {note.id} добавлена в базу данных")

    def get_all_notes(self) -> list[Note]:
        notes = [Note.from_json(item) for item in self.notes.values()]
        logging.info(f"Запрос на получение всех заметок")
        return notes

    def get_note_by_id(self, id: str) -> Note:
        if id not in self.notes:
            logging.error(f"Заметки с ID {id} нет")
            return
        note = Note.from_json(self.notes[id])
        logging.info(f"Запрос на получение заметки с ID {id}")
        return note

    def edit_note(self, note: Note) -> None:
        if note.id not in self.notes:
            logging.error(f"Заметки с ID {id} нет")
            return
        self.notes[note.id] = note.to_json()
        self.save_to_file()
        logging.info(f"Запрос на изменение заметки с ID {note.id}")

    def delete_note(self, id: str) -> None:
        if id not in self.notes:
            logging.error(f"Заметки с ID {id} нет")
            return
        del self.notes[id]
        self.save_to_file()
        logging.info(f"Заметка с ID {id} удалена")

    def export_to_csv(self, filename: str) -> None:
        df = pd.DataFrame.from_dict(self.notes)

        df = df.transpose().reset_index(drop=True)
        df.to_csv(filename, index=False)

    def import_from_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        df.index = df["id"]
        data = df.to_dict("index")
        self.notes = data
        self.save_to_file()


class TaskManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.init_tasks()

    def init_tasks(self) -> None:
        if not os.path.isfile(self.filename):
            logging.warning(f"Файл {self.filename} не найден")
            with open(self.filename, "w") as file:
                file.write("{}")
                logging.info(f"Файл {self.filename} создан")
            self.tasks = {}
        else:
            with open(self.filename, "r+") as file:
                try:
                    tasks = json.loads(file.read())
                    logging.info(
                        f"Файл {self.filename} найден и является валидным JSON"
                    )
                    self.tasks = tasks
                except:
                    logging.warning(f"Файл {self.filename} поврежден")
                    file.seek(0)
                    file.truncate(0)
                    file.write("{}")
                    logging.info(f"Файл {self.filename} перезаписан")
                    self.tasks = {}

    def save_to_file(self) -> None:
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.tasks))

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task.to_json()
        self.save_to_file()
        logging.info(f"Задача с ID {task.id} добавлена")

    def get_all_tasks(self) -> list[Task]:
        logging.info("Запрос на получение всех задач")
        return [Task.from_json(item) for item in self.tasks.values()]

    def get_task_by_id(self, task_id: str) -> Task:
        if task_id not in self.tasks:
            logging.error(f"Задачи с ID {task_id} нет")
            return None
        logging.info(f"Запрос на получение задачи с ID {task_id}")
        return Task.from_json(self.tasks[task_id])

    def edit_task(self, updated_task: Task) -> None:
        if updated_task.id not in self.tasks:
            logging.error(f"Задачи с ID {updated_task.id} нет")
            return
        self.tasks[updated_task.id] = updated_task.to_json()
        self.save_to_file()
        logging.info(f"Задача с ID {updated_task.id} обновлена")

    def delete_task(self, task_id: str) -> None:
        if task_id not in self.tasks:
            logging.error(f"Задачи с ID {task_id} нет")
            return
        del self.tasks[task_id]
        self.save_to_file()
        logging.info(f"Задача с ID {task_id} удалена")

    def export_to_csv(self, filename: str) -> None:
        df = pd.DataFrame.from_dict(self.tasks, orient="index")
        df.to_csv(filename, index=False)
        logging.info(f"Задачи экспортированы в файл {filename}")

    def import_from_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        df.index = df["id"]
        self.tasks = df.to_dict("index")
        self.save_to_file()
        logging.info(f"Задачи импортированы из файла {filename}")

    def filter_tasks(self, status=None, priority=None, due_date=None) -> list[Task]:
        tasks = self.get_all_tasks()
        if status is not None:
            tasks = [task for task in tasks if task.done == status]
        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]
        if due_date is not None:
            tasks = [task for task in tasks if task.due_date == due_date]
        return tasks


class ContactManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.init_contacts()

    def init_contacts(self) -> None:
        if not os.path.isfile(self.filename):
            logging.warning(f"Файл {self.filename} не найден")
            with open(self.filename, "w") as file:
                file.write("{}")
                logging.info(f"Файл {self.filename} создан")
            self.contacts = {}
        else:
            with open(self.filename, "r+") as file:
                try:
                    contacts = json.loads(file.read())
                    logging.info(
                        f"Файл {self.filename} найден и является валидным JSON"
                    )
                    self.contacts = contacts
                except:
                    logging.warning(f"Файл {self.filename} поврежден")
                    file.seek(0)
                    file.truncate(0)
                    file.write("{}")
                    logging.info(f"Файл {self.filename} перезаписан")
                    self.contacts = {}

    def save_to_file(self) -> None:
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.contacts))

    def add_contact(self, contact: Contact) -> None:
        self.contacts[contact.id] = contact.to_json()
        self.save_to_file()
        logging.info(f"Контакт с ID {contact.id} добавлен")

    def get_all_contacts(self) -> list[Contact]:
        logging.info("Запрос на получение всех контактов")
        return [Contact.from_json(item) for item in self.contacts.values()]

    def search_contact(self, query: str) -> list[Contact]:
        results = [
            Contact.from_json(contact)
            for contact in self.contacts.values()
            if query.lower() in contact["name"].lower() or query in contact["phone"]
        ]
        logging.info(f"Поиск контактов по запросу '{query}'")
        return results

    def edit_contact(self, updated_contact: Contact) -> None:
        if updated_contact.id not in self.contacts:
            logging.error(f"Контакт с ID {updated_contact.id} не найден")
            return
        self.contacts[updated_contact.id] = updated_contact.to_json()
        self.save_to_file()
        logging.info(f"Контакт с ID {updated_contact.id} обновлён")

    def delete_contact(self, contact_id: str) -> None:
        if contact_id not in self.contacts:
            logging.error(f"Контакт с ID {contact_id} не найден")
            return
        del self.contacts[contact_id]
        self.save_to_file()
        logging.info(f"Контакт с ID {contact_id} удалён")

    def export_to_csv(self, filename: str) -> None:
        df = pd.DataFrame.from_dict(self.contacts, orient="index")
        df.to_csv(filename, index=False)
        logging.info(f"Контакты экспортированы в файл {filename}")

    def import_from_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        df.index = df["id"]
        self.contacts = df.to_dict("index")
        self.save_to_file()
        logging.info(f"Контакты импортированы из файла {filename}")


class FinanceManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.init_records()

    def init_records(self) -> None:
        if not os.path.isfile(self.filename):
            logging.warning(f"Файл {self.filename} не найден")
            with open(self.filename, "w") as file:
                file.write("{}")
                logging.info(f"Файл {self.filename} создан")
            self.records = {}
        else:
            with open(self.filename, "r+") as file:
                try:
                    records = json.loads(file.read())
                    logging.info(
                        f"Файл {self.filename} найден и является валидным JSON"
                    )
                    self.records = records
                except:
                    logging.warning(f"Файл {self.filename} поврежден")
                    file.seek(0)
                    file.truncate(0)
                    file.write("{}")
                    logging.info(f"Файл {self.filename} перезаписан")
                    self.records = {}

    def save_to_file(self) -> None:
        with open(self.filename, "w") as file:
            file.write(json.dumps(self.records))

    def add_record(self, record: FinanceRecord) -> None:
        self.records[record.id] = record.to_json()
        self.save_to_file()
        logging.info(f"Финансовая запись с ID {record.id} добавлена")

    def get_all_records(self) -> list[FinanceRecord]:
        logging.info("Запрос на получение всех финансовых записей")
        return [FinanceRecord.from_json(item) for item in self.records.values()]

    def filter_records(self, category=None, date=None) -> list[FinanceRecord]:
        records = self.get_all_records()
        if category is not None:
            records = [record for record in records if record.category == category]
        if date is not None:
            records = [record for record in records if record.date == date]
        return records

    def calculate_balance(self) -> float:
        balance = sum(record.amount for record in self.get_all_records())
        logging.info(f"Общий баланс: {balance} руб.")
        return balance

    def generate_report(self, start_date=None, end_date=None):
        records = self.get_all_records()
        if start_date:
            records = [
                record
                for record in records
                if datetime.strptime(record.date, "%d-%m-%Y")
                >= datetime.strptime(start_date, "%d-%m-%Y")
            ]
        if end_date:
            records = [
                record
                for record in records
                if datetime.strptime(record.date, "%d-%m-%Y")
                <= datetime.strptime(end_date, "%d-%m-%Y")
            ]

        report = {}
        for record in records:
            if record.category not in report:
                report[record.category] = 0
            report[record.category] += record.amount

        logging.info("Отчёт о финансовой активности сгенерирован")
        return report

    def delete_record(self, record_id: str) -> None:
        if record_id not in self.records:
            logging.error(f"Запись с ID {record_id} не найдена")
            return
        del self.records[record_id]
        self.save_to_file()
        logging.info(f"Финансовая запись с ID {record_id} удалена")

    def export_to_csv(self, filename: str) -> None:
        df = pd.DataFrame.from_dict(self.records, orient="index")
        df.to_csv(filename, index=False)
        logging.info(f"Финансовые записи экспортированы в файл {filename}")

    def import_from_csv(self, filename: str) -> None:
        df = pd.read_csv(filename)
        df.index = df["id"]
        self.records = df.to_dict("index")
        self.save_to_file()
        logging.info(f"Финансовые записи импортированы из файла {filename}")
