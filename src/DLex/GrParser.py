from .lexer import *


class LexParser:
    def __init__(self, text=None) -> None:
        self.text = text
        self.dfa: DFA
        self.row = 0
        self.col = 0

    def genNFA(self, nfa, text):
        cnt = 0
        for line in text.readlines():
            arr = line.split()
            if len(arr) < 3 or arr[0] == '#':
                continue
            if arr[0] not in nfa.nodes:
                nfa.nodes[arr[0]] = Node()
            if arr[0] == Start:
                nfa.starts.append(arr[3])
            if len(arr) == 3 and arr[2] == 'E':
                nfa.nodes[arr[0]].isEnd = True
                cnt += 1
            else:
                if arr[3] not in nfa.mp:
                    nfa.mp[arr[3]] = {}
                    nfa.nodes[arr[3]] = Node()
                if arr[0] not in nfa.mp:
                    nfa.mp[arr[0]] = {arr[2]: [arr[3]]}
                else:
                    if arr[2] not in nfa.mp[arr[0]]:
                        nfa.mp[arr[0]][arr[2]] = [arr[3]]
                    else:
                        nfa.mp[arr[0]][arr[2]].append(arr[3])
        for u in nfa.mp:
            if len(nfa.mp[u]) == 0:
                nfa.nodes[u].isEnd = True
        for it in nfa.starts:
            nfa.nodes[it].types.add(it)
        q = [Start]
        vis = {Start}
        while len(q) > 0:
            u = q.pop(0)
            for e in nfa.mp[u]:
                for v in nfa.mp[u][e]:
                    nfa.nodes[v].types |= nfa.nodes[u].types
                    if v not in vis:
                        vis.add(v)
                        q.append(v)

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
    nfa = NFA()
    lp = LexParser(code)
    lp.genNFA(nfa, text)
    lp.dfa = DFA(nfa)
    for it in lp.parse():
        print('row:'+str(it.row) + ',col:' +
              str(it.col)+',value:' + str(it.value))


if __name__ == '__main__':
    main()
