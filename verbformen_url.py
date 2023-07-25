from word import *

class VerbformenURL:
    __VERBFORMEN_URL = "https://www.verbformen.de"
    
    @staticmethod
    def build(word: Word) -> str:
        if isinstance(word, Noun): 
            endpoint = f"/deklination/substantive/grundform/der_{word.value}.mp3"
        elif isinstance(word, Verb):
            endpoint = f"/konjugation/infinitiv/{word.value}.mp3"
        elif isinstance(word, Adjective):
            endpoint = f"/deklination/adjektive/grundform/{word.value}.mp3"
        return VerbformenURL.__VERBFORMEN_URL + endpoint
