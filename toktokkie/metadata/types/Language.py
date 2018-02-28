class Language:
    """
    Class that parses ISO 639-2/B language codes
    """

    languages = {
        "eng": "English",
        "ger": "German",
        "jpn": "Japanese",
        "ita": "Italian",
        "spa": "Spanish",
        "fre": "French",
        "chi": "Chinese",
        "kor": "Korean",
        "rus": "Russian"
    }  # TODO Implement more languages

    def __init__(self, identifier: str):
        if identifier.lower() not in self.languages:
            raise ValueError(identifier)
        self.language = identifier.lower()

    def get_language_name(self) -> str:
        return self.languages[self.language]

    def __str__(self) -> str:
        return self.language
