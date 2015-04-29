from unidecode import unidecode


class Normalizer:

    def normalize(text):
        text = Normalizer.remove_extra_whitespaces(text)
        text = Normalizer.replace_hyphens(text)
        # text = Normalizer.remove_accent_marks(text)

        return text.lower()

    @staticmethod
    def replace_hyphens(text):
        return text.replace('-', ' ')

    @staticmethod
    def remove_extra_whitespaces(text):
        return ' '.join(text.strip().split());

    @staticmethod
    def remove_accent_marks(text):
        return unidecode(text)