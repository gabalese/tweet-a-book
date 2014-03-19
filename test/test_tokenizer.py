import unittest
import urllib2
import os
from tempfile import NamedTemporaryFile
from src.functions import tokenize, html_to_text

from src.epub import EPUB


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        remotefile = urllib2.urlopen('http://dev.alese.it/book/urn:uuid:c72fb312-f83e-11e2-82c4-001cc0a62c0b/download')
        self.testfile = NamedTemporaryFile(delete=True)
        self.testfile.write(remotefile.read())

    def testcorrectinstantiation(self):
        epub = EPUB(self.testfile)
        self.assertIsInstance(epub, EPUB)

    def testmanifest(self):
        epub = EPUB(self.testfile)
        self.assertGreaterEqual(len(epub.manifest), 1)

    def testtotextfunction(self):
        epub = EPUB(self.testfile)
        for k in epub.manifest:
            if k.attrib["media-type"] == "application/xhtml+xml":
                self.assertIsNotNone(epub.read(os.path.join(os.path.dirname(epub.opf_path), k.attrib["href"])))
                break

    def testtokenizer(self):
        epub = EPUB(self.testfile)
        listtokens = []
        for k in epub.manifest:
            if k.attrib["media-type"] == "application/xhtml+xml":
                plaintext = html_to_text(epub.read(os.path.join(os.path.dirname(epub.opf_path), k.attrib["href"])))
                if len(tokenize(plaintext)) > 0:
                    listtokens.extend(tokenize(plaintext))
        self.assertGreaterEqual(len(listtokens), 1)

if __name__ == '__main__':
    unittest.main()
