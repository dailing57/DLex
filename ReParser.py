import re
from lexer import *


class RegexParser:
    def __init__(self, regRule) -> None:
        self.regRule = regRule


class LexParser:
    def nextChar(self, ch: str):
        pass

    def genNFA(self, nfa, text):
        pass
