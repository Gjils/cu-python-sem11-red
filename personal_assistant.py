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