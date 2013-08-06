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
        self.user_store = session.client.get_user_store()
        self.note_store = session.client.get_note_store()
        self.session = session

    def test_connect(self):
        user = self.user_store.getUser()
        self.assertEqual(user.username, 'hhrhakuna')
    
    def test_get_notebook_by_name(self):
        notebook = self.session.get_notebook_by_name('python')
        guid = notebook.guid
        self.assertEqual(guid, '58481245-136a-4cf8-ad70-4fe40909909a')



if __name__ == '__main__':
    main()