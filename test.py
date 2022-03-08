import lexer


def main():
    text = open('rule.txt', encoding='utf-8')
    dfa = lexer.DFA(text)
    lexio = lexer.LexIO()
    lexio.DFAwrite('DFAresult.txt', dfa)
    dfa = lexio.DFALoad('DFAresult.txt', dfa)
    print(dfa)


if __name__ == '__main__':
    main()
