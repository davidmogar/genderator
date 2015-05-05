import unicodedata

good_accents = {
    u'\N{LATIN CAPITAL LETTER N WITH TILDE}',
    u'\N{LATIN SMALL LETTER N WITH TILDE}',
    u'\N{LATIN CAPITAL LETTER C WITH CEDILLA}',
    u'\N{LATIN SMALL LETTER C WITH CEDILLA}'
}


class Normalizer:

    def normalize(text, options={}):
        """
        Normalize a given text applying all normalizations.

        Params:
            text: The text to be processed.

        Returns:
            The text normalized.
        """
        if options.get('whitespaces', True):
            text = Normalizer.remove_extra_whitespaces(text)

        if options.get('hyphens', True):
            text = Normalizer.replace_hyphens(text)

        accents = options.get('hyphens', True)
        symbols = options.get('symbols', True)

        if accents and symbols:
            text = Normalizer.normalize_unicode(text)
        elif accents:
            text = Normalizer.remove_accent_marks(text)
        else:
            text = Normalizer.remove_symbols(text)

        return text.lower()

    @staticmethod
    def normalize_unicode(text):
        """
        Remove accent marks and symbols from input text.

        This function has the same effect that remove_accent_marks and remove_symbols but use a single loop.

        Params:
            text: The text to be processed.

        Returns:
            The text without accent marks and symbols.
        """
        categories = ['Mn', 'Sc', 'Sk', 'Sm', 'So']

        return ''.join(c for c in unicodedata.normalize('NFKC', text)
                       if unicodedata.category(c) not in categories or c in good_accents)

    @staticmethod
    def remove_accent_marks(text):
        """
        Remove accent marks from input text.

        Params:
            text: The text to be processed.

        Returns:
            The text without accent marks.
        """
        return ''.join(c for c in unicodedata.normalize('NFKC', text)
                       if unicodedata.category(c) != 'Mn' or c in good_accents)

    @staticmethod
    def remove_extra_whitespaces(text):
        """
        Remove extra whitespaces from input text.

        This function removes whitespaces from the beginning and the end of
        the string, but also duplicated whitespaces between words.

        Params:
            text: The text to be processed.

        Returns:
            The text without extra whitespaces.
        """
        return ' '.join(text.strip().split())

    @staticmethod
    def replace_hyphens(text):
        """
        Remove hyphens from input text.

        Params:
            text: The text to be processed.

        Returns:
            The text without hyphens.
        """
        return text.replace('-', ' ')

    @staticmethod
    def remove_symbols(text):
        """
        Remove symbols from input text.

        Params:
            text: The text to be processed.

        Returns:
            The text without symbols.
        """
        return ''.join(c for c in unicodedata.normalize('NFKC', text)
                       if unicodedata.category(c) != 'Mn' or c in good_accents)
