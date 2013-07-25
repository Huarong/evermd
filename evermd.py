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


class CreateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, '<!--\ntitle: \nnotebook: \ntags: \n-->\n\n')


class MarkdownComplier(object):
    def __init__(self, markdown_path):
        tmpdir = tempfile.gettempdir()
        self.name = os.path.basename(markdown_path).split('.')[0]
        self.html_path = os.path.join(tmpdir, '%s.html' % self.name)
        markdown.markdownFromFile(input=markdown_path, output=self.html_path)
        self.html = open(self.html_path, 'rb')
        self.html_string = self.html.read()


class UploadeCommand(sublime_plugin.TextCommand):
    def __init__(self):
        super(UploadeCommand, self)__init__()

    def connect(self):
        pass

    def upload(self):
        region.view.