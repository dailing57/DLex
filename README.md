# DLex
DL‘s Lexer

使用方法：

通过三型文法获得一个持久化的DFA pickle文件：DFAresult

```powershell
python .\LexIO.py .\rule.txt pickle
```

对于DFAresult，可以进行画图：

```powershell
python .\genfa.py .\DFAresult sDFA
```

也可以直接通过输入三型文法来获得一个NFA或者最小化DFA

```powershell
python .\genfa.py .\rule.txt NFA
```

```powershell
python .\genfa.py .\rule.txt D
```

