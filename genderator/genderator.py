import os

path = os.path.dirname(__file__)


class Genderator:

    __names, __ratios = {}, {}
    __surnames = []

    def __init__(self):
        self.__load_data()

    def __load_data(self):
        """
        Load all data files into memory.
        """
        self.__load_names()
        self.__load_name_surname_ratios()
        self.__load_surnames()

    def __load_names(self):
        """
        Load names data file.

        This file contains a list of spanish given names with the probability for
        each one to be a male or female name.
        """
        with open(os.path.join(path, 'data/names_ine')) as file:
            for line in file:
                if not line.startswith('#'):
                    (name, prob_female, prob_male) = line.rstrip().split('\t')
                    self.__names[name] = float(prob_male)

    def __load_name_surname_ratios(self):
        """
        Load name/surnames ratios data file.

        The file contains a list of names and surnames with the probability for each
        one to be a name (lower values) or a surname (higher values).
        """
        with open(os.path.join(path, 'data/name_surname_ratio')) as file:
            for line in file:
                if not line.startswith('#'):
                    (key, val) = line.rstrip().split('\t')
                    self.__ratios[key] = float(val)

    def __load_surnames(self):
        """
        Load names data file.

        This file contains a list of spanish surnames.
        """
        with open(os.path.join(path, 'data/surnames_ine')) as file:
            for line in file:
                if not line.startswith('#'):
                    self.__surnames.append(line.rstrip())

    def parse(self, fullname):
        return self.__normalize(fullname)

    def __normalize(self, text):
        """
        Normalize input text transforming it to lowercase, removing hyphens,
        whitespaces from both sides and extra whitespaces between words.

        Params:
            text: String to be normalized.

        Returns:
            Normalized text.
        """
        return ' '.join(text.lower().replace('-', ' ').strip().split())