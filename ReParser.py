import json
from lexer import *
from genfa import FAVisualizer


class ReParserError(Error):
    pass


class RegexParser:
    def __init__(self, regRule=None) -> None:
        self.regRule = regRule
        self.nfa = NFA()
        self.pos = 0
        self.curChar = regRule[0]
        self.tot = 0

    def nextChar(self, ch):
        assert(self.curChar == ch)
        self.pos += 1
        if self.pos >= len(self.regRule):
            self.curChar = None
        else:
            self.curChar = self.regRule[self.pos]
        return self.curChar

    def peekChar(self):
        if self.pos + 1 < len(self.regRule) + 1:
            return self.regRule[self.pos + 1]
        else:
            return None

    def range(self, fa):
        while(self.curChar is not None and self.curChar != ']'):
            if self.curChar == '\\':
                self.nextChar(self.curChar)
            if self.peekChar() == '-':
                l = self.curChar
                self.nextChar(self.curChar)
                self.nextChar('-')
                r = ''
                if self.curChar == '\\':
                    r = self.nextChar(self.curChar)
                else:
                    r = self.curChar
                self.nextChar(self.curChar)
                for i in range(ord(l), ord(r)+1):
                    self.nfa.link(fa, chr(i), self.tot)
            else:
                self.nfa.link(fa, self.curChar, self.tot)
                self.nextChar(self.curChar)
        if self.curChar is None:
            raise ReParserError(message='Unexpected EOF')

    def factor(self, fa):
        self.tot += 1
        ans = self.tot
        if self.curChar == '\\':
            self.nextChar('\\')
            self.nfa.link(fa, self.curChar, self.tot)
            self.nextChar(self.curChar)
        elif self.curChar == '[':
            self.nextChar('[')
            self.range(fa)
            self.nextChar(']')
        elif self.curChar == '(':
            self.nextChar('(')
            self.nfa.link(fa, Epsilon, self.tot)
            ans = self.expr(self.tot)
            self.nextChar(')')
        elif self.curChar is not None:
            if self.curChar == '*' or self.curChar == '+' or self.curChar == '?':
                raise RecursionError(
                    message='Unexpected Letter {curChar}'.format(curChar=self.curChar))
            self.nfa.link(fa, self.curChar, self.tot)
            self.nextChar(self.curChar)
        return ans

    def term(self, fa):
        tot = self.factor(fa)
        if self.curChar == '*':
            self.tot += 1
            self.nfa.link(tot, Epsilon, fa)
            self.nfa.link(tot, Epsilon, self.tot)
            self.nfa.link(fa, Epsilon, self.tot)
            self.nextChar('*')
            return self.tot
        elif self.curChar == '+':
            self.tot += 1
            self.nfa.link(tot, Epsilon, fa)
            self.nfa.link(tot, Epsilon, self.tot)
            self.nextChar('+')
            return self.tot
        elif self.curChar == '?':
            self.nfa.link(fa, Epsilon, tot)
            self.nextChar('?')
        return tot

    def termList(self, fa):
        tot = self.term(fa)
        while self.curChar is not None and self.curChar != '|' and self.curChar != ')':
            tot = self.term(tot)
        return tot

    def expr(self, fa):
        tot = self.termList(fa)
        self.tot += 1
        self.nfa.link(tot, Epsilon, self.tot)
        while self.curChar is not None and self.curChar == '|':
            self.nextChar('|')
            tmp = self.termList(fa)
            self.nfa.link(tmp, Epsilon, self.tot)
        return self.tot

    def genNFA(self):
        self.tot += 1
        self.nfa.link(Start, Epsilon, self.tot)
        ed = self.expr(self.tot)
        self.nfa.nodes[ed].isEnd = True
        return self.nfa


class RegexRuleConfig:
    def __init__(self, config) -> None:
        self.rules = json.load(config)

    def parseRule(self):
        for it in self.rules:
            rp = RegexParser(self.rules[it])
            self.rules[it] = DFA(rp.genNFA())


class LexParser:
    pass


def main():
    config = open('config.json', 'r')
    rr = RegexRuleConfig(config)
    nfa = RegexParser(rr.rules['SCIENCE']).genNFA()
    nfaVis = FAVisualizer(dfa=DFA(nfa))
    nfaVis.bfsD()
    nfaVis.dot.view('NFA')


if __name__ == '__main__':
    main()
