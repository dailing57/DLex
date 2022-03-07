from tkinter import N
from lexer import NFA, DFA
import argparse
from graphviz import Digraph


class FAVisualizer:
    def __init__(self, nfa={}, dfa={}) -> None:
        self.nfa = nfa
        self.dfa = dfa
        self.dot = Digraph(name="NFA", node_attr={
            "shape": "circle",
            "fontsize": "12",
            "fontname": "Courier", "height": ".1"
        },
            edge_attr={"arrowsize": ".5"},
            format="png",
            graph_attr={"ranksep": ".3", "layout": "dot"})

    def bfsN(self):
        q = ['S']
        vis = set('S')
        while(len(q) > 0):
            u = q.pop(0)
            for e in self.nfa.mp[u]:
                for v in self.nfa.mp[u][e]:
                    self.dot.edge(u, v, label=e)
                    if (v not in vis) and (v != 'E'):
                        q.append(v)
                        vis.add(v)
        for it in self.nfa.nodes:
            if self.nfa.nodes[it].isEnd:
                self.dot.node(it, shape='doublecircle')
        print(len(vis))

    def bfsD(self):
        q = [self.dfa.root]
        vis = {self.dfa.root: 1}
        cnt = 1
        while len(q) > 0:
            u = q.pop(0)
            for e in self.dfa.dfa[u]:
                v = self.dfa.dfa[u][e]
                if v not in vis:
                    cnt += 1
                    vis[v] = cnt
                    q.append(v)
                self.dot.edge(str(vis[u]), str(vis[v]), label=e)
        for it in self.dfa.ends:
            self.dot.node(str(vis[it]), shape='doublecircle')


def main():
    parser = argparse.ArgumentParser(
        description='Draw the FA graph'
    )
    parser.add_argument('inputfile', help='rule file')
    parser.add_argument('mode', help='NFA or DFA')
    args = parser.parse_args()
    text = open(args.inputfile, encoding='utf-8')
    if(args.mode == 'NFA'):
        nfa = NFA(text)
        nfaVis = FAVisualizer(nfa=nfa)
        nfaVis.bfsN()
        nfaVis.dot.view('NFA')
    if(args.mode == 'DFA'):
        dfa = DFA(text)
        dfaVis = FAVisualizer(dfa=dfa)
        dfaVis.bfsD()
        dfaVis.dot.view('DFA')


if __name__ == '__main__':
    main()
