# encoding: utf-8
# author: Huarong Huo

import os
import os.path
import tempfile
import sublime
import sublime_plugin
import markdown
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors


class CreateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, '<!--\ntitle: \nnotebook: \ntags: \n-->\n\n')


class UploadeCommand(sublime_plugin.TextCommand):
    def __init__(self):
        super(UploadeCommand, self).__init__()
        self.token = ''
        self.client = None

    def get_markdown(self):
        region = sublime.Region(0, self.view.size())
        markdown_string = self.view.substr(region)
        return markdown_string

    def markdown_to_html(self):
        markdown_string = get_markdown(self)
        html_string = markdown.markdown(markdown_contents)
        return html_string

    def connect_evernote(self, token="S=s1:U=71d19:E=147661e4de8:C=1400e6d21ea:P=1cd:A=en-devtoken:V=2:H=57b60a9b8c031aa3a1333ff591c1aa25"):
        client = EvernoteClient(token=token)
        self.token = token
        self.client = client

    def create_dir(self):
        """Create a notebook named Evermd to store markdown source code if not exist"""
        noteStore = self.client.get_note_store()
        notebook = Types.Notebook()
        notebook.name = 'Evermd'
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

    def run(self):
        self.connect_evernote()
        self.create_dir()
        self.upload('hello, sublime text 2!')
