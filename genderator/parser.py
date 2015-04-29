import codecs
import json
import os

from collections import OrderedDict
from .utils import Normalizer

path = os.path.dirname(__file__)


class Parser:
    __names, __ratios = {}, {}
    __surnames = []

    def __init__(self):
        self._load_data()

    def _load_data(self):
        """
        Load all data files into memory.
        """
        self._load_names()
        self._load_name_surname_ratios()
        self._load_surnames()

    def _load_names(self):
        """
        Load names data file.

        This file contains a list of spanish given names with the probability for
        each one to be a male or female name.
        """
        for line in self.remove_file_comments('names_ine'):
                (name, prob_female, prob_male) = line.rstrip().split('\t')
                self.__names[name] = float(prob_male)

    def _load_name_surname_ratios(self):
        """
        Load name/surnames ratios data file.

        The file contains a list of names and surnames with the probability for each
        one to be a name (lower values) or a surname (higher values).
        """
        for line in self.remove_file_comments('name_surname_ratio'):
            (key, val) = line.rstrip().split('\t')
            self.__ratios[key] = float(val)

    def _load_surnames(self):
        """
        Load names data file.

        This file contains a list of spanish surnames.
        """
        for line in self.remove_file_comments('surnames_ine'):
            self.__surnames.append(line.rstrip())

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

    def guess_gender(self, fullname):
        if isinstance(fullname, str):
            fullname = Normalizer.normalize(fullname)
            names, surnames = self._classify(fullname)

            if names and surnames:
                real_name, ratio = self._get_gender_ratio(list(names.keys()))
                return self._create_answer(real_name, ratio, names, surnames)
            pass

    def _classify(self, fullname):
        """
        Classify fullname tokens into names and surnames based on datasets.

        Params:
            fullname: Full name to be classified.

        Returns:
            Two OrderedDicts of names and surnames with its confidence ratio.
        """
        name_complete = False
        names, surnames = OrderedDict(), OrderedDict()

        for word in fullname.split():
            if word in self.__ratios:
                # If word could be a name or surname
                ratio = self.__ratios[word]
                if not names or (ratio < 0.5 and not name_complete):
                    names[word] = 1 - ratio
                else:
                    surnames[word] = ratio
                    if ratio == 1:
                        name_complete = True
            else:
                if word in self.__names:
                    if not name_complete:
                        names[word] = 1
                elif word in self.__surnames:
                    surnames[word] = 1
                    name_complete = True

        return names, surnames

    def _get_gender_ratio(self, names):
        """
        Returns the male/female ratio for the given names.

        To do this, the function compute possible names combining items on the list
        and try to form the longest name possible.

        The value returned go from 0 to 1. Values near to 1 represent a higher possibility
        of the evaluated name to be a male name.

        Params:
            names: List of names.

        Returns:
            The longest name computed by combining items in the list,
            and the male/female ratio.
        """
        for i in range(len(names), 0, -1):
            real_name = ' '.join(names[:i])
            if real_name in self.__names:
                return real_name, self.__names[real_name]

    def _create_answer(self, real_name, ratio, names, surnames):
        """
        Process computed data and generated a JSON answer.

        Params:
            real_name: Real name (computed name) extracted from the original text.
            ratio: Male/female ratio.
            names: Names identified on the original text.
            surnames: Surnames identified on the original text.

        Returns:
            A JSON string with all the computed information.
        """
        answer = OrderedDict()
        answer['names'] = names
        answer['surnames'] = surnames
        answer['real_name'] = real_name
        male = ratio > 0.5
        answer['gender'] = 'Male' if male else 'Female'
        answer['confidence'] = ratio if male else 1 - ratio
        return json.dumps(answer)