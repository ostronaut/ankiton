from typing import Union
from word import *
import re


class WordMatcher:
    @staticmethod
    def match(line: str) -> Union[None, Word]:
        def matched_word(Word) -> Union[None, Word]:
            r = re.match(Word.regex(), line)
            return Word(r.group(1)) if r else None

        return next(
            (
                value
                for value in [matched_word(Noun), matched_word(Verb), matched_word(Adjective)]
                if value is not None
            ),
            None,
        )
