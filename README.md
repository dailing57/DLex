# DLex
DL‘s Lexer

使用方法：

通过三型文法获得一个持久化的DFA pickle文件：DFAresult

```powershell
python .\LexIO.py .\test\rule.txt pickle
```

对于DFAresult，可以进行画图：

```powershell
python .\genfa.py .\test\DFAresult sDFA
```

也可以直接通过输入三型文法来获得一个NFA或者最小化DFA

```powershell
python .\genfa.py .\test\rule.txt NFA
```

```powershell
python .\genfa.py .\test\rule.txt D
```

通过同时输入三型文法和代码获得token流

```powershell
python .\GrParser.py .\test\rule.txt .\test\testcode
```

