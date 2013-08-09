# encoding: utf-8
# author: Huarong Huo

import sys
from unittest import TestCase, main

sys.path.append('../lib')
sys.path.append('../')

from evernote_session import EvernoteSession


class EvernoteSessionTest(TestCase):
    def setUp(self):
        session = EvernoteSession()
        session.connect()
        self.session = session

    def test_connect(self):
        user = self.session.user_store.getUser()
        self.assertEqual(user.username, 'hhrhakuna')
    
    def test_get_notebook_by_name(self):
        notebook = self.session.get_notebook_by_name('python')
        guid = notebook.guid
        self.assertEqual(guid, '58481245-136a-4cf8-ad70-4fe40909909a')

    def test_create_notebook(self):
        name = '__test_create_notebook__'
        created_nb = self.session.create_notebook(name)
        got_nb = self.session.get_notebook_by_name(name)
        self.assertEqual(created_nb.guid, got_nb.guid)
        self.session.note_store.expungeNotebook(created_nb.guid)


    def test_get_meta_info(self):
        with open('test_get_meta_info.md', 'rb') as f:
            content = f.read()
        got_meta_info = self.session.get_meta_info(content)
        required_meta_info = {'title': 'test get meta info',
            'tagNames': ['test', 'meta_info', 'Lady Gaga'],
            'notebookGuid': 'fc166263-9a43-4c4c-a0c0-7640c70dedc3'
        }
        self.assertEqual(got_meta_info, required_meta_info)

    def test_get_note(self):
        guid = '0979ef10-87e7-4ddb-bf11-4a2e63469ae3'
        note = self.session.get_note(guid)
        self.assertEqual(note.title, 'test get note')
        self.assertEqual(note.content, '<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n\
<en-note><div>This is a test note for get_note method</div></en-note>')

    def test_post_note(self):
        with open('test_post_note.md', 'rb') as f:
            content = f.read()
        meta_info = self.session.get_meta_info(content)
        posted_note = self.session.post_note(meta_info, content)
        got_note = self.session.get_note(posted_note.guid)
        self.assertEqual(posted_note.title, got_note.title)
        self.session.note_store.expungeNote(got_note.guid)


    def test_update_note(self):
        with open('test_update_note.md', 'rb') as f:
            content = f.read()
        guid = '1f059de7-2a0b-4fce-9f39-65820fcee8e7'
        meta_info = self.session.get_meta_info(content)
        note = self.session.get_note(guid)
        self.assertEqual(note.title, 'test update note [before update]')
        self.assertEqual(self.session.note_store.getNoteTagNames(guid), ['update'])
        self.session.update_note(guid, meta_info, content)
        updated_note = self.session.get_note(guid)
        self.assertEqual(updated_note.title, 'test update note [after update]')
        self.assertEqual(self.session.note_store.getNoteTagNames(guid), ['update', 'after'])
        roll_back_note = updated_note
        roll_back_note.title = 'test update note [before update]'
        # roll_back_note.tagNames = ['update']
        tagguid = self.session.get_tag_by_name('update')
        roll_back_note.tagGuids = [tagguid]
        self.session.note_store.updateNote(roll_back_note)



if __name__ == '__main__':
    main()