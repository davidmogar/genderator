from unittest import TestCase

import codecs
import os
import genderator

path = os.path.dirname(__file__)

DELTA = 0.01
MAX_PERCENTAGE_ERROR = 0.05
TEST_FILE_LINES = 100000


class TestParser(TestCase):
    __data = {}
    __parser = genderator.Parser()

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

    def test_gender_guessing(self):
        """
        Check if mistake percentage is lower than MAX_ERROR_PERCENTAGE while guessing gender.
        """
        mistakes = 0
        for line in self.remove_file_comments('valid_names.tsv'):
            (name, first_surname, second_surname, male_probability) = line.split('\t')
            fullname = ' '.join([name, first_surname, second_surname])
            answer = self.__parser.guess_gender(fullname)
            confidence = float(answer['confidence'])
            calculated_male_probability = confidence if answer['gender'] == 'Male' else 1 - confidence

            if abs(calculated_male_probability - float(male_probability)) > DELTA:
                mistakes += 1
            self.assertLess(mistakes / TEST_FILE_LINES * 100, MAX_PERCENTAGE_ERROR,
                            'Mistakes percentage greater than ' + str(MAX_PERCENTAGE_ERROR))

    def test_match(self):
        """
        Check if there is a match for every full name in the test file.
        """
        for line in self.remove_file_comments('valid_names.tsv'):
            (name, first_surname, second_surname, male_probability) = line.split('\t')
            fullname = ' '.join([name, first_surname, second_surname])
            answer = self.__parser.guess_gender(fullname)
            self.assertIsNotNone(answer, 'Fullname doesn\'t match: ' + fullname)

    def test_name_guessing(self):
        """
        Check if mistake percentage is lower than MAX_ERROR_PERCENTAGE while guessing name.
        """
        mistakes = 0
        for line in self.remove_file_comments('valid_names.tsv'):
            (name, first_surname, second_surname, male_probability) = line.split('\t')
            fullname = ' '.join([name, first_surname, second_surname])
            answer = self.__parser.guess_gender(fullname)
            try:
                if answer['real_name'] != name:
                    mistakes += 1
                self.assertLess(mistakes / TEST_FILE_LINES * 100, MAX_PERCENTAGE_ERROR,
                                'Mistakes percentage greater than ' + str(MAX_PERCENTAGE_ERROR))
            except TypeError:
                print(fullname)