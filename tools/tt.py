from graphviz import Digraph
import random
from copy import deepcopy


class Part:
    def __init__(self, src, edge, dst):
        self.src = src
        self.edge = edge
        self.dst = dst


def move(DFA, src, edge):
    for i in range(len(DFA)):
        if DFA[i].src[0] == src and DFA[i].edge == edge:
            return DFA[i].dst[0]
    return ''


def get_source_set(target_set, char, DFA):
    global allstatus
    allstatusSet = set(allstatus)
    source_set = set()
    for state in allstatusSet:
        try:
            if move(DFA, state, char) in target_set:
                source_set.update(state)
        except KeyError:
            pass
    return source_set


def hopcroft_algorithm(DFA):
    global sigma
    global endSet
    global allstatus
    cins = set(sigma)
    termination_states = set(endSet)
    total_states = set(allstatus)
    not_termination_states = total_states - termination_states

    P = [termination_states, not_termination_states]
    W = [termination_states, not_termination_states]

    while W:

        A = random.choice(W)
        W.remove(A)

        for char in cins:
            X = get_source_set(A, char, DFA)
            P_temp = []

            for Y in P:
                S = X & Y
                S1 = Y - X

                if len(S) and len(S1):
                    P_temp.append(S)
                    P_temp.append(S1)

                    if Y in W:
                        W.remove(Y)
                        W.append(S)
                        W.append(S1)
                    else:
                        if len(S) <= len(S1):
                            W.append(S)
                        else:
                            W.append(S1)
                else:
                    P_temp.append(Y)
            P = deepcopy(P_temp)
    return P


def indexMinList(minList, a):
    for i in range(len(minList)):
        if a in minList[i]:
            return i
    return ''


DFA = []
DFA2 = []
DFADic = {}
sigma = ['a', 'b']
# dot = Digraph(comment='The Test Table')
dot = Digraph("DFA")
num = int(input('input:'))
for i in range(num):
    x = input()
    y = input()
    z = input()
    temp = []
    temp.append(x)
    temp.append(y)
    DFA2.append(temp)
    DFADic[tuple(temp)] = y
    temp = Part(x, y, z)
    DFA.append(temp)
    if i == 1:
        dot.node(name=x, color='blue')
        dot.edge(x, z, y)
    else:
        dot.node(name=x, color='black')
        dot.edge(x, z, y)

for i in range(len(DFA)):
    print(DFA[i].src, DFA[i].edge, DFA[i].dst)

endSet = []
endNum = int(input('input end num:'))
for i in range(endNum):
    temp = input()
    endSet.append(temp)

startSet = []
allSet = []

for i in range(len(DFA)):
    if DFA[i].src[0] not in endSet:
        startSet.append(DFA[i].src[0])
    if DFA[i].dst[0] not in endSet:
        startSet.append(DFA[i].src[0])

allstatus = startSet
allstatus.extend(endSet)
dot.render('DFA.gv', view=True)
minList = hopcroft_algorithm(DFA)
minDFA = []
print(minList)


for i in range(len(minList)):
    dstList = [0, 0]  # 用来存储每种状态经过a和b变换后的结果
    for j in range(len(minList[i])):
        listi = list(minList[i])
        if dstList[0] == 0 and move(DFA, listi[j], sigma[0]) != '' and indexMinList(minList, move(DFA, listi[j], sigma[0])) != '':
            print(indexMinList(minList, move(DFA, listi[j], sigma[0])))
            dstList[0] = min(minList[indexMinList(
                minList, move(DFA, listi[j], sigma[0]))])
            # 使用Min函数的原因是为了重新给每种状态命名，选去每个状态中的最小的即可

        if dstList[1] == 0 and move(DFA, listi[j], sigma[1]) != '' and indexMinList(minList, move(DFA, listi[j], sigma[1])) != '':
            dstList[1] = min(minList[indexMinList(
                minList, move(DFA, listi[j], sigma[1]))])
    if dstList[0] != 0:
        temp = Part(min(minList[i]), 'a', dstList[0])
        minDFA.append(temp)
    if dstList[1] != 0:
        temp2 = Part(min(minList[i]), 'b', dstList[1])
        minDFA.append(temp2)


dot2 = Digraph('测试图片')

for i in range(len(minDFA)):
    print(minDFA[i].src, minDFA[i].edge, minDFA[i].dst)
    if i == 1:
        dot2.node(name=minDFA[i].src, color='red')
        dot2.edge(minDFA[i].src, minDFA[i].dst, minDFA[i].edge)
    else:
        dot2.node(name=minDFA[i].src, color='black')
        dot2.edge(minDFA[i].src, minDFA[i].dst, minDFA[i].edge)

dot2.render('minDFA.gv', view=True)
