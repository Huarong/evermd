# encoding: utf-8
# author: Huarong Huo

import sys
from unittest import TestCase, main
import markdown

sys.path.append('../')
from evermd import MarkdownComplier


class MarkdownTest(TestCase):
    def test_markdown_compiler(self):
        markdown_file = 'markdown.md'
        html_file = 'markdown.html'
        mdc = MarkdownComplier(markdown_file)
        self.assertEqual(mdc.name, 'markdown')
        with open(html_file, 'rb') as html:
            self.assertEqual(mdc.html_string, html.read())


if __name__ == '__main__':
    main()
