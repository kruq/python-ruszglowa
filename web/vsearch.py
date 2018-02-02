def search4letters(phrase: str, letters: str = "aeiouy") -> str:
    """Search for letters inside the phrase"""
    return set(phrase).intersection(set(letters))

