from .lexer import *
import argparse
from .GrParser import LexParser
from graphviz import Digraph
from . import LexIO


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
        q = [Start]
        vis = set(Start)
        while(len(q) > 0):
            u = q.pop(0)
            for e in self.nfa.mp[u]:
                for v in self.nfa.mp[u][e]:
                    if e == '\\':
                        e = '\\\\'
                    self.dot.edge(str(u), str(v), label=e)
                    if (v not in vis):
                        q.append(v)
                        vis.add(v)
        for it in self.nfa.nodes:
            if self.nfa.nodes[it].isEnd:
                self.dot.node(str(it), shape='doublecircle')

    def bfsD(self):
        q = [self.dfa.root]
        vis = {self.dfa.root}
        while len(q) > 0:
            u = q.pop(0)
            for e in self.dfa.dfa[u]:
                v = self.dfa.dfa[u][e]
                if v not in vis:
                    vis.add(v)
                    q.append(v)
                if e == '\\':
                    e = '\\\\'
                self.dot.edge(str(u), str(v), label=e)
        for it in self.dfa.ends:
            self.dot.node(str(it), shape='doublecircle')


def main():
    parser = argparse.ArgumentParser(
        description='Draw the FA graph'
    )
    parser.add_argument('inputfile', help='rule file')
    parser.add_argument(
        'mode', help='NFA or DFA or sDFA (serialized DFA pickle file)')
    args = parser.parse_args()
    if(args.mode == 'NFA'):
        text = open(args.inputfile, encoding='utf-8')
        nfa = NFA()
        LexParser().genNFA(nfa=nfa, text=text)
        nfaVis = FAVisualizer(nfa=nfa)
        nfaVis.bfsN()
        nfaVis.dot.view('NFA')
    elif(args.mode == 'DFA'):
        text = open(args.inputfile, encoding='utf-8')
        nfa = NFA()
        LexParser().genNFA(nfa, text)
        dfa = DFA(nfa)
        dfaVis = FAVisualizer(dfa=dfa)
        dfaVis.bfsD()
        dfaVis.dot.view('DFA')
    elif(args.mode == 'sDFA'):
        dfa = LexIO.readPickle(args.inputfile)
        dfaVis = FAVisualizer(dfa=dfa)
        dfaVis.bfsD()
        dfaVis.dot.view('DFA')


if __name__ == '__main__':
    main()
