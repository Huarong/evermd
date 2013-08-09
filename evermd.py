# encoding: utf-8
# author: Huarong Huo

import sys
sys.path.insert(0, 'lib/')
print sys.path
import os
import os.path
import tempfile
import sublime
import sublime_plugin
import markdown
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
from evernote_session import EvernoteSession

class CreateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, '<!--\ntitle: \nnotebook: \ntags: \n-->\n\n')

class UploadCommand(sublime_plugin.TextCommand):
    def run(self):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        self.send_to_evernote(content)

    def send_to_evernote(self, content):
        session = EvernoteSession()
        session.connect()
        meta_info = session.get_meta_info(content)
        session.post_note(meta_info, content)


