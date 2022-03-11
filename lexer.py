import argparse
from distutils.log import error


class Token:
    def __init__(self, col=-1, row=-1, type=set(), value='') -> None:
        self.col = col
        self.row = row
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.row,
            column=self.col,
        )

    def __repr__(self) -> str:
        return self.__str__()


class Node:
    def __init__(self, isEnd=False) -> None:
        self.isEnd = isEnd
        self.types = set()

    def __str__(self) -> str:
        return 'Node(isEnd:{isEnd},types:{types})\n'.format(
            types=self.types,
            isEnd=self.isEnd
        )

    def __repr__(self) -> str:
        return self.__str__()


class NFA:
    def __init__(self, text) -> None:
        self.mp = {}
        self.nodes = {}
        self.starts = []
        self.parse(text)

    def parse(self, text):
        cnt = 0
        for line in text.readlines():
            arr = line.split()
            if len(arr) < 3 or arr[0] == '#':
                continue
            if arr[0] not in self.nodes:
                self.nodes[arr[0]] = Node()
            if arr[0] == 'S':
                self.starts.append(arr[3])
            if len(arr) == 3 and arr[2] == 'E':
                self.nodes[arr[0]].isEnd = True
                cnt += 1
            else:
                if arr[3] not in self.mp:
                    self.mp[arr[3]] = {}
                    self.nodes[arr[3]] = Node()
                if arr[0] not in self.mp:
                    self.mp[arr[0]] = {arr[2]: [arr[3]]}
                else:
                    if arr[2] not in self.mp[arr[0]]:
                        self.mp[arr[0]][arr[2]] = [arr[3]]
                    else:
                        self.mp[arr[0]][arr[2]].append(arr[3])
        for u in self.mp:
            if len(self.mp[u]) == 0:
                self.nodes[u].isEnd = True
        for it in self.starts:
            self.nodes[it].types.add(it)
        q = ['S']
        vis = {'S'}
        while len(q) > 0:
            u = q.pop(0)
            for e in self.mp[u]:
                for v in self.mp[u][e]:
                    self.nodes[v].types |= self.nodes[u].types
                    if v not in vis:
                        vis.add(v)
                        q.append(v)


class DFA(NFA):
    def __init__(self, text) -> None:
        super(DFA, self).__init__(text)
        self.dfa = {}
        self.DNodes = {}
        self.root = frozenset()
        self.ends = set()
        self.NtoD()
        self.minimize()

    def emClosure(self, st):
        res = set()
        q = []
        for u in st:
            res.add(u)
            q.append(u)
        while len(q) > 0:
            u = q.pop(0)
            if 'EMP' in self.mp[u]:
                for v in self.mp[u]['EMP']:
                    if v not in res:
                        res.add(v)
                        q.append(v)
        return res

    def NtoD(self):
        rt = frozenset(self.emClosure({'S'}))
        vis = {rt}
        q = [rt]
        self.root = rt
        while len(q) > 0:
            st = q.pop(0)
            for it in st:
                if(self.nodes[it].isEnd):
                    self.ends.add(st)
            if st not in self.dfa:
                self.dfa[st] = {}
            stE = set()
            for u in st:
                for e in self.mp[u]:
                    if e == 'EMP':
                        continue
                    stE.add(e)
                    if e not in self.dfa[st]:
                        self.dfa[st][e] = set()
                    for v in self.mp[u][e]:
                        self.dfa[st][e].add(v)
            for e in stE:
                self.dfa[st][e] = frozenset(self.emClosure(self.dfa[st][e]))
                fst = self.dfa[st][e]
                if fst not in vis:
                    q.append(fst)
                    vis.add(fst)

    def minimize(self):
        edges = set()
        for u in self.dfa:
            for e in self.dfa[u]:
                if e != 'EMP':
                    edges.add(e)
        st = set()
        startst = set()
        fends = frozenset(self.ends)
        st.add(fends)
        for it in self.dfa:
            if it not in self.ends:
                startst.add(it)
        fstartst = frozenset(startst)
        st.add(fstartst)
        # Hopcroft
        W = {fstartst}
        while len(W) > 0:
            A = W.pop()
            for e in edges:
                X = set()
                for u in self.dfa:
                    if e in self.dfa[u] and self.dfa[u][e] in A:
                        X.add(u)
                tmp = st.copy()
                X = frozenset(X)
                for Y in st:
                    YaX = frozenset(X & Y)
                    YsX = frozenset(Y - X)
                    if len(YaX) > 0 and len(YsX) > 0:
                        tmp.remove(Y)
                        tmp.add(YaX)
                        tmp.add(YsX)
                        if Y in W:
                            W.remove(Y)
                            W.add(YaX)
                            W.add(YsX)
                        else:
                            if len(YaX) <= len(YsX):
                                W.add(YaX)
                            else:
                                W.add(YsX)
                st = tmp

        # 处理最终的集合
        tmp = {}
        tot = 0
        for it in st:
            tot += 1
            isStart = False
            cur = Node()
            for u in it:
                if u == self.root:
                    isStart = True
                for v in u:
                    cur.types |= self.nodes[v].types
                    cur.isEnd = cur.isEnd or self.nodes[v].isEnd
            for u in it:
                tmp[u] = tot
                self.DNodes[tot] = cur
            if isStart:
                self.root = tot
        newDfa = {}
        for it in st:
            for u in it:
                if tmp[u] not in newDfa:
                    newDfa[tmp[u]] = {}
                for e in self.dfa[u]:
                    v = self.dfa[u][e]
                    newDfa[tmp[u]][e] = tmp[v]
                    if tmp[v] not in newDfa:
                        newDfa[tmp[v]] = {}
        self.dfa = newDfa
        self.ends = set()
        for it in self.DNodes:
            if self.DNodes[it].isEnd:
                self.ends.add(it)


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        self.message = f'{self.__class__.__name__}: {message}'


class LexerError(Error):
    pass


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


if __name__ == '__main__':
    main()
