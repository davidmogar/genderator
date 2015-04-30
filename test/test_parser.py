from unittest import TestCase

import codecs
import os
from genderator.parser import Parser

path = os.path.dirname(__file__)

class TestParser(TestCase):
    __names = set()
    __surnames = set()

    def setUp(self):
        for line in self.remove_file_comments('names_ine'):
            self.__names.add(line.split('\t')[0])

        for line in self.remove_file_comments('surnames_ine'):
            self.__surnames.add(line)

        for line in self.remove_file_comments('name_surname_ratio'):
            word = line.split('\t')[0]
            self.__names.add(word)
            self.__surnames.add(word)

    def remove_file_comments(self, relative_path):
        """
        Generator to remove comments from a file.

        Params:
            file: File to be processed.
        """
        with codecs.open(os.path.join(path, 'data', relative_path), 'r', 'UTF-8') as file:
            for line in file:
                line = line.strip()
                if not line.startswith('#'):
                    yield line