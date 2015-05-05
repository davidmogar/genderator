import codecs
import os

from collections import OrderedDict
from .utils import Normalizer

path = os.path.dirname(__file__)


class Parser:
    """
    This class offers a simple way to parse Spanish name (from Spain), classifying
    names and surnames and detecting the given name gender.

    Attributes:
        force_combinations (boolean): Force combinations during classification.
        force_split (boolean): Force name split if no surnames detected.
        normalize (boolean): Enable or disable normalization.
        normalizer_options (dict): Normalizer options to be applied.
    """
    __names, __ratios = {}, {}
    __surnames = []

    def __init__(self, force_combinations=True, force_split=True, normalize=True, normalizer_options={}):
        self.__force_combinations = force_combinations
        self.__force_split = force_split
        self.__normalize = normalize
        self.__normalizer_options = normalizer_options

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
        for line in self.remove_file_comments('names_ine.tsv'):
                (name, frequency, prob_male) = line.split('\t')
                self.__names[name] = float(prob_male)

    def _load_name_surname_ratios(self):
        """
        Load name/surnames ratios data file.

        The file contains a list of names and surnames with the probability for each
        one to be a name (lower values) or a surname (higher values).
        """
        for line in self.remove_file_comments('name_surname_ratio.tsv'):
            (key, val) = line.split('\t')
            self.__ratios[key] = float(val)

    def _load_surnames(self):
        """
        Load names data file.

        This file contains a list of spanish surnames.
        """
        for line in self.remove_file_comments('surnames_ine.tsv'):
            self.__surnames.append(line.split('\t')[0])

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
        """
        Guess the gender of the given full name.

        Params:
            fullname: Full name from where we want to guess the gender.

        Returns:
            A JSON string with all the computed information.
        """
        if isinstance(fullname, str):
            if self.__normalize:
                fullname = Normalizer.normalize(fullname, self.__normalizer_options)

            names, surnames = self._classify(fullname)

            if names and (surnames or (self.__force_split and self._is_splittable(names))):
                real_name, ratio = self._get_gender_ratio(list(names))
                return self._create_answer(real_name, ratio, names, surnames)

    def _is_splittable(self, names):
        """
        Check if a list of names can be splitted in names and surnames.

        Params:
            names: List of name to be checked.

        Returns:
            True if can be splitted or false otherwise.
        """
        names_iterator = iter(names)
        next(names_iterator)
        for name in names_iterator:
            if name in self.__ratios and self.__ratios[name] < 1: return True
        return False

    def _classify(self, fullname):
        """
        Split fullname into tokens and classify them into names and surnames based on datasets.

        Params:
            fullname: Full name to be classified.

        Returns:
            Two lists, one with names and the other with surnames.
        """
        names, surnames = [], []
        unclassified = []
        processed = []

        for word in fullname.split():
            combination_result = None

            if self.__force_combinations:
                combination_result = self._combine_words(processed, word, names)

            if combination_result is None:
                keep_going = True
                if unclassified:
                    if self._classify_word(unclassified[-1] + ' ' + word, names, surnames, unclassified):
                        keep_going = False
                if keep_going:
                    if unclassified:
                        self._classify_word(word, names, surnames)
                    else:
                        self._classify_word(word, names, surnames, unclassified)

                processed.append(word)

        return names, surnames

    def _combine_words(self, processed, word, names):
        """
        Try to combine last processed word with the word received as parameter.

        If the combination of both words is a name, this is added to the list, replacing
        the name added previously.

        Params:
            processed: List of words already processed.
            word: Current word.
            names: List of classified names.

        Returns:
            A valid combination if found or None otherwise.
        """
        if processed and names:
            last_word = processed[-1]
            if last_word == names[-1]:
                combination = last_word + ' ' + word
                if combination in self.__names:
                    names.pop(names.index(last_word))
                    names.append(combination)
                    processed[-1] = combination
                    return combination
        return None

    def _classify_word(self, word, names, surnames, unclassified=None):
        """
        Try to classify a word in name or surname based on datasets.

        Params:
            word: Word to be classified.
            names: List of classified names.
            surnames: List of classified surnames.
            unclassified: List of words without match.

        Returns:
            True if the word was classified. False otherwise.
        """
        classified = True

        if word in self.__ratios:
            if (not names or self.__ratios[word] > 0.5) and not surnames:
                names.append(word)
            else:
                surnames.append(word)
        else:
            if word in self.__surnames and names:
                surnames.append(word)
            elif word in self.__names and not surnames:
                names.append(word)
            else:
                if unclassified is not None:
                    unclassified.append(word)
                classified = False

        if classified and unclassified is not None: unclassified.clear()

        return classified

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
        return answer