
from YAMS.parser import Parser

with open("asm/example1.s") as f:
    parser = Parser(f.read())
    d, t = parser.parse()
    print(d)
    print(t)