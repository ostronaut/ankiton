import logging
import sys
import os
import re
from typing import List
from requests.exceptions import HTTPError

from word_matcher import WordMatcher
from verbformen_url import VerbformenURL
from url_request import URLRequest
from anki import Anki
from word import Word


def main(source_file: str, mp3_dir: str):
    with open(source_file, "r") as file:
        lines = file.readlines()

    processed_lines = process_lines(lines, mp3_dir)

    with open(source_file, "w") as file:
        file.write("".join(processed_lines))


def process_lines(lines: List[str], mp3_dir: str) -> List[str]:
    adjusted_lines = []
    for line in lines:
        maybe_word = None if _has_mp3_reference(line) else WordMatcher.match(line)
        if maybe_word:
            url = VerbformenURL.build(_adjust_word_for_url(maybe_word))
            mp3_path = os.path.join(mp3_dir, f"{maybe_word.value}.mp3")
            try:
                URLRequest(url).request_save_mp3(mp3_path)
                Anki.upload_media_file(mp3_path)
                adjusted_lines.append(
                    _add_mp3_reference(line, os.path.basename(mp3_path))
                )
                logging.info(f"loaded mp3 for {maybe_word}")
            except HTTPError:
                logging.warn(f"can not load mp3 for {maybe_word}, url is {url}")
                adjusted_lines.append(line)
        else:
            adjusted_lines.append(line)
    else:
        return adjusted_lines


def _has_mp3_reference(line: str) -> bool:
    regex = "^.*!\[\[.*\.mp3\]\].*$"
    return bool(re.match(regex, line))


def _add_mp3_reference(line: str, mp3_ref: str) -> str:
    regex = "^(.{3,}?)#.*$"
    match = re.search(regex, line)
    return line[: match.end(1)] + f"![[{mp3_ref}]] " + line[match.end(1) :]


def _adjust_word_for_url(word: Word) -> Word:
    return word.__class__(
        word.value.replace("ü", "u3")
        .replace("ä", "a3")
        .replace("ö", "o3")
        .replace("ß", "s5")
    )


if __name__ == "__main__":
    source_file = sys.argv[1]
    mp3_dir = os.path.join(os.path.dirname(source_file), "Audios")

    main(source_file, mp3_dir)
