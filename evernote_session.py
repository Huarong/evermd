# encoding: utf-8
# author: Huarong Huo

import sys
sys.path.insert(0, 'lib/')
print sys.path
import os
import os.path
import re
import logging
import tempfile
import markdown
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from utils import text_to_ENML

class EvernoteSession(object):
    def __init__(self):
        self.token = 'S=s1:U=71d19:E=147661e4de8:C=1400e6d21ea:P=1cd:A=en-devtoken:V=2:H=57b60a9b8c031aa3a1333ff591c1aa25'
        self.client = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect(self, token=''):
        if token:
            self.token = token
        client = EvernoteClient(token=self.token)
        self.client = client

    def get_notebook_by_name(self, name):
        note_store = self.client.get_note_store()
        notebooks = note_store.listNotebooks()
        for nb in notebooks:
            if nb.name == name:
                return nb
        return None

    def create_notebook(self, name):
        """Create a notebook if not exist"""
        if self.get_notebook_by_name(name):
            return False
        note_store = self.client.get_note_store()
        notebook = Types.Notebook()
        notebook.name = name
        try:
            notebook = note_store.createNotebook(notebook)
            return notebook
        except Errors.EDAMUserException, e:
            self.logger.error(e)
            return False

    def get_meta_info(self, content):
        meta_info = {}
        pattern = re.compile('<!--(.*?)-->', re.DOTALL)
        result = pattern.search(content)
        if not result:
            return meta_info
        meta_str = result.group(1)
        # {'name in content': 'name in evernote note attribute'}
        valid_field = {'title': 'title', 'tags': 'tagNames', 'notebook': 'notebookGuid'}
        lines = meta_str.split(os.linesep)
        pattern = re.compile('^(.+?):(.+?)$')
        for line in lines:
            if not line:
                continue
            result = pattern.match(line)
            if not result:
                continue
            field = result.group(1).strip()
            value = result.group(2).strip()
            if field in valid_field:
                if field == 'tags':
                    value = [v.strip() for v in value.split(',')]
                if field == 'notebook':
                    value = self.get_notebook_by_name(value).guid
                meta_info[valid_field[field]] = value
        return meta_info

    def get_note(self, guid):
        note_store = self.client.get_note_store()
        return note_store.getNote(guid, True, False, False, False)

    def post_note(self, meta_info, content):
        note_store = self.client.get_note_store()
        note = Types.Note()
        for k, v in meta_info.items():
            setattr(note, k, v)
        note.content = text_to_ENML(content)
        note = note_store.createNote(note)
        return note

    def update_note(self, guid, meta_info, content):
        note = self.get_note(guid)
        for k, v in meta_info.items():
            setattr(note, k, v)
        note.content = text_to_ENML(content)
        note_store = self.client.get_note_store()
        note_store.updateNote(note)
        return note

