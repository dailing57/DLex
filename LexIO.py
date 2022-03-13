import lexer
import pickle
import argparse


def writePickle(text):
    dfa = lexer.DFA(text)
    with open('DFAresult', 'wb') as f:
        pickle.dump(dfa, f)


def readPickle(inputfile):
    with open(inputfile, 'rb') as pkf:
        return pickle.load(pkf)


def main():
    parser = argparse.ArgumentParser(
        description='serialization about dfa'
    )
    parser.add_argument('inputfile', help='rule file')
    parser.add_argument('mode', help='pickle or yaml')
    args = parser.parse_args()
    if args.mode == 'pickle':
        text = open(args.inputfile, encoding='utf-8')
        writePickle(text)
        text.close()


if __name__ == '__main__':
    main()
