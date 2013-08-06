# encoding: utf-8
# author: Huarong Huo

import sys
sys.path.insert(0, 'lib/')
print sys.path
import os
import os.path
import tempfile
import markdown
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

class EvernoteSession(object):
    def __init__(self):
        self.token = 'S=s1:U=71d19:E=147661e4de8:C=1400e6d21ea:P=1cd:A=en-devtoken:V=2:H=57b60a9b8c031aa3a1333ff591c1aa25'
        self.client = None

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

    def dir_exist(self):
        note_store = self.client.get_note_store()


    def create_dir(self):
        """Create a notebook named __evermd__ to store markdown source code if not exist"""
        noteStore = self.client.get_note_store()
        notebook = Types.Notebook()
        notebook.name = '__evermd__'
        try:
            notebook = noteStore.createNotebook(notebook)
            return notebook.guid
        except Errors.Errors.EDAMUserException,e:
            sublime.error_message('Error %s' % e)

    def upload(self, content):
        noteStore = self.client.get_note_store()
        note = Types.Note()
        note.title = 'hello'
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>%s</en-note>' % content
        note = note_store.createNote(note)