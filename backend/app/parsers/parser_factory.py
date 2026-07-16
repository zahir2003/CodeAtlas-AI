from app.parsers.language_detector import LanguageDetector


class ParserFactory:

    @staticmethod
    def get_language(file_path):

        return LanguageDetector.detect(file_path)