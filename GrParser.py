from lexer import *


class LexParser:
    def __init__(self, text, dfa) -> None:
        self.text = text
        self.dfa: DFA = dfa
        self.row = 0
        self.col = 0

    def error(self, curChar):
        s = "Lexer error on '{lexeme}' line: {row} column: {col}".format(
            lexeme=curChar,
            row=self.row,
            col=self.col,
        )
        raise LexerError(message=s)

    def next(self, curState, curChar):
        if curChar in self.dfa.dfa[curState]:
            return self.dfa.dfa[curState][curChar]
        else:
            if self.dfa.DNodes[curState].isEnd:
                return 0
            else:
                self.error(curChar=curChar)

    def parse(self):
        tokens = []
        try:
            curState = self.dfa.root
            curChar = ''
            for line in self.text.readlines():
                self.row += 1
                self.col = 0
                while self.col < len(line) and line[self.col].isspace():
                    self.col += 1
                tk = Token(col=self.col, row=self.row, value='')
                while self.col < len(line):
                    curChar = line[self.col]
                    tmp = self.next(curState, curChar=curChar)
                    if tmp == 0:
                        tk.type = self.dfa.DNodes[curState].types
                        tokens.append(tk)
                        curState = self.dfa.root
                        tk = Token(col=self.col, row=self.row, value='')
                        while self.col < len(line) and line[self.col].isspace():
                            self.col += 1
                    else:
                        curState = tmp
                        tk.type &= self.dfa.DNodes[curState].types
                        tk.value += line[self.col]
                        self.col += 1
                if curChar == '\n':
                    continue
                tmp = self.next(curState, None)
                if tmp == 0:
                    tk.type = self.dfa.DNodes[curState].types
                    tokens.append(tk)
                    curState = self.dfa.root
                    tk = Token(col=self.col, row=self.row, value='')

        except LexerError as e:
            print(e.message)
        return tokens


def main():
    parser = argparse.ArgumentParser(
        description='DLex - DL\'s Lexer'
    )
    parser.add_argument('rulefile', help='rule file')
    parser.add_argument('codefile', help='code file')
    args = parser.parse_args()
    text = open(args.rulefile, 'r')
    code = open(args.codefile, 'r')
    dfa = DFA(text)
    lp = LexParser(code, dfa)
    for it in lp.parse():
        print('row:'+str(it.row) + ',col:' +
              str(it.col)+',value:' + str(it.value))


if __name__ == '__main__':
    main()
