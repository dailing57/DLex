import argparse
import sys


class Token:
    def __init__(self) -> None:
        self.col = 0
        self.row = 0
        self.type = ''
        self.value = ''

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.row,
            column=self.col,
        )

    def __repr__(self) -> str:
        return self.__str__()


class NFANode:
    def __init__(self, isEnd=False) -> None:
        self.isEnd = isEnd


class NFA:
    def __init__(self, text) -> None:
        self.mp = {}
        self.nodes = {}
        self.starts = []
        self.parse(text)

    def parse(self, text):
        for line in text.readlines():
            arr = line.split()
            if len(arr) < 3 or arr[0] == '#':
                continue
            if arr[0] == 'S':
                self.starts.append(arr[3])
            if arr[0] not in self.nodes:
                self.nodes[arr[0]] = NFANode()
            if len(arr) == 3 and arr[2] == 'E':
                self.nodes[arr[0]].isEnd = True
            elif arr[0] not in self.mp:
                self.mp[arr[0]] = {arr[2]: [arr[3]]}
            else:
                if arr[2] not in self.mp[arr[0]]:
                    self.mp[arr[0]][arr[2]] = [arr[3]]
                else:
                    self.mp[arr[0]][arr[2]].append(arr[3])
        self.nodes['E'] = NFANode(isEnd=True)


def main():
    parser = argparse.ArgumentParser(
        description='DLex - DL\'s Lexer'
    )
    parser.add_argument('inputfile', help='rule file')
    args = parser.parse_args()
    text = open(args.inputfile, 'r')
    nfa = NFA(text)


if __name__ == '__main__':
    main()
