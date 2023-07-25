from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Word(ABC):
    value: str

    @staticmethod
    @abstractmethod
    def regex():
        ...


@dataclass
class Noun(Word):
    @staticmethod
    def regex():
        return "^### Deutsche: (?:der|die|das) ([A-Za-zäöüÄÖÜß]+).*#Substativ.*$"


@dataclass
class Verb(Word):
    @staticmethod
    def regex():
        return "^### Deutsche: ([A-Za-zäöüÄÖÜß]+).*#verb.*$"


@dataclass
class Adjective(Word):
    @staticmethod
    def regex():
        return "^### Deutsche: ([A-Za-zäöüÄÖÜß]+).*#Adjektive.*$"
