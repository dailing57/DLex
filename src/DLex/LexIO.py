import pickle


def writePickle(dfa):
    with open('DFAresult', 'wb') as f:
        pickle.dump(dfa, f)


def readPickle(inputfile):
    with open(inputfile, 'rb') as pkf:
        return pickle.load(pkf)


def main():
    pass


if __name__ == '__main__':
    main()
