
from YAMS.parser import Parser
from YAMS.assembler import Assembler

with open("asm/simple_jump.s") as f:
    parser = Parser(f.read())
    d, t = parser.parse()
    print("BEFORE ASSEMBLY")
    print(t)
    assembler = Assembler(t, d)
    assembler.assemble()
    print("AFTER ASSEMBLING")
    print(assembler.text_segment)