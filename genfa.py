from lexer import NFA
import argparse
from graphviz import Digraph


class NFAVisualizer:
    def __init__(self, nfa) -> None:
        self.nfa = nfa
        self.dot = Digraph(name="NFA", node_attr={
            "shape": "circle",
            "fontsize": "12",
            "fontname": "Courier", "height": ".1"
        },
            edge_attr={"arrowsize": ".5"},
            format="png",
            graph_attr={"ranksep": ".3", "layout": "dot"})

    def bfs(self):
        q = []
        vis = set()
        self.dot.node(name="S")
        for it in self.nfa.starts:
            self.dot.edge('S', it)
            q.append(it)
            vis.add(it)
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


def main():
    parser = argparse.ArgumentParser(
        description='Draw the FA graph'
    )
    parser.add_argument('inputfile', help='rule file')
    args = parser.parse_args()
    text = open(args.inputfile, encoding='utf-8')
    nfa = NFA(text)
    nfaVis = NFAVisualizer(nfa)
    nfaVis.bfs()
    nfaVis.dot.view('NFA')


if __name__ == '__main__':
    main()
