a = {frozenset({'7'}), frozenset({'5'}), frozenset({'6'})}
b = {frozenset({'5'}), frozenset({'3'}), frozenset({'6'})}


p = frozenset({frozenset({'7'})})
q = frozenset({frozenset({'5'}), frozenset({'7'})})
print(p & q)
