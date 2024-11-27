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
