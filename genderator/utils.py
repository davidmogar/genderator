from unidecode import unidecode


class Normalizer:

    def normalize(text):
        """
        Normalize a given text applying all normalizations.

        Params:
            text: The text to be processed.

        Returns:
            The text normalized.
        """
        text = Normalizer.remove_extra_whitespaces(text)
        text = Normalizer.replace_hyphens(text)
        text = Normalizer.remove_accent_marks(text)

        return text.lower()

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
        return ' '.join(text.strip().split());

    @staticmethod
    def remove_accent_marks(text):
        """
        Remove accent marks from input text.

        Params:
            text: The text to be processed.

        Returns:
            The text without accent marks.
        """
        return unidecode(text)