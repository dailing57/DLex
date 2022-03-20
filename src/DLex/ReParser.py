import json
from .lexer import *


class ReParserError(Error):
    pass


class RegexParser:
    def __init__(self, regRule=None) -> None:
        self.regRule = regRule
        self.nfa = NFA(mp={}, nodes={}, starts=[])
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
        ed = self.tot
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
                    self.nfa.link(fa, chr(i), ed)
            elif self.curChar == '(':
                self.nextChar('(')
                self.tot += 1
                self.nfa.link(fa, Epsilon, self.tot)
                tmp = self.expr(self.tot)
                self.nfa.link(tmp, Epsilon, ed)
                self.nextChar(')')
            else:
                self.nfa.link(fa, self.curChar, ed)
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
        ed = self.tot
        self.nfa.link(tot, Epsilon, ed)
        while self.curChar is not None and self.curChar == '|':
            self.nextChar('|')
            tmp = self.termList(fa)
            self.nfa.link(tmp, Epsilon, ed)
        return ed

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
    def __init__(self, config) -> None:
        rrc = RegexRuleConfig(config)
        rrc.parseRule()
        self.rrc = rrc.rules
        self.row = 0
        self.col = 0

    def next(self, cur, c):
        tmp = {}
        for it in cur:
            u = cur[it]
            if c in self.rrc[it].dfa[u]:
                tmp[it] = self.rrc[it].dfa[u][c]
        return tmp

    def error(self, curChar):
        s = "Lexer error on '{lexeme}' line: {row} column: {col}".format(
            lexeme=curChar,
            row=self.row,
            col=self.col,
        )
        raise LexerError(message=s)

    def parse(self, code):
        cur = {}
        tokens = []
        for it in self.rrc:
            cur[it] = self.rrc[it].root
        try:
            for line in code.readlines():
                self.row += 1
                self.col = 0
                while self.col < len(line) and line[self.col].isspace():
                    self.col += 1
                tk = Token()
                c = ''
                while self.col < len(line):
                    c = line[self.col]
                    tmp = self.next(cur, c)
                    if len(tmp) == 0:
                        curEnds = []
                        for it in cur:
                            u = cur[it]
                            if self.rrc[it].DNodes[u].isEnd:
                                curEnds.append(it)
                        for it in curEnds:
                            if len(curEnds) > 1:
                                if it != 'ID':
                                    tk.type = it
                            else:
                                tk.type = it
                        if tk.type == set():
                            self.error(c)
                        tk.col = self.col
                        tk.row = self.row
                        tokens.append(tk)
                        tk = Token()
                        for it in self.rrc:
                            cur[it] = self.rrc[it].root
                        while self.col < len(line) and line[self.col].isspace():
                            self.col += 1
                    else:
                        cur = tmp
                        tk.value += c
                        self.col += 1
                if c != '\n':
                    curEnds = []
                    for it in cur:
                        u = cur[it]
                        if self.rrc[it].DNodes[u].isEnd:
                            curEnds.append(it)
                    for it in curEnds:
                        if len(curEnds) > 1:
                            if it != 'ID':
                                tk.type = it
                        else:
                            tk.type = it
                    if tk.type == set():
                        self.error(c)
                    tk.col = self.col
                    tk.row = self.row
                    tokens.append(tk)
        except LexerError as e:
            print(e.message)
        return tokens


def main():
    config = open('config.json', 'r')
    code = open('./test/testcode', 'r')
    lp = LexParser(config)
    tokens = lp.parse(code)
    for it in tokens:
        print(it)


if __name__ == '__main__':
    main()
