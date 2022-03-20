import argparse
from . import ReParser
from . import GrParser
from . import LexIO
from . import genfa
from . import lexer


def main():
    parser = argparse.ArgumentParser(
        description='DLex - DL\'s Lexer'
    )
    ruleType = parser.add_mutually_exclusive_group(required=True)
    ruleType.add_argument("-g", "--gramma", action="store_true",
                          help='parse rule by gramma method')
    ruleType.add_argument("-r", "--regex", action="store_true",
                          help='parse rule by regex method')
    parser.add_argument('rulefile', help='rule file', default='config.json')
    operationType = parser.add_mutually_exclusive_group(required=True)
    operationType.add_argument(
        "-d", "--draw", action="store_true", help="draw DFA")
    parser.add_argument(
        "-type", help="the type of the regex DFA", default='')
    operationType.add_argument(
        "-p", '--parse', action="store_true", help='parse the code and output token stream')
    parser.add_argument('-codefile',
                        help='code file', default='./test/testcode')
    operationType.add_argument(
        '-pk', '--pickle', action="store_true", help='serialize the dfa')
    args = parser.parse_args()
    rulefile = open(args.rulefile, 'r')
    lp = None
    if args.gramma:
        lp = GrParser.LexParser()
        nfa = lexer.NFA()
        lp.genNFA(nfa, rulefile)
        lp.dfa = lexer.DFA(nfa)
        if args.draw:
            dfaVis = genfa.FAVisualizer(dfa=lp.dfa)
            dfaVis.bfsD()
            dfaVis.dot.view('DFA')
        elif args.parse:
            codefile = open(args.codefile, 'r')
            lp.text = codefile
            for it in lp.parse():
                print('row:'+str(it.row) + ',col:' +
                      str(it.col)+',value:' + str(it.value))
        elif args.pickle:
            LexIO.writePickle(lp.dfa)
    elif args.regex:
        lp = ReParser.LexParser(rulefile)
        if args.draw:
            dfaVis = genfa.FAVisualizer(dfa=lp.rrc[args.type])
            dfaVis.bfsD()
            dfaVis.dot.view('DFA')
        elif args.parse:
            codefile = open(args.codefile, 'r')
            for it in lp.parse(codefile):
                print(it)
        elif args.pickle:
            LexIO.writePickle(lp.rrc)


if __name__ == '__main__':
    main()
