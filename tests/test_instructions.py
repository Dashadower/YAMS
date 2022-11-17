
from YAMS.parser import Parser
from YAMS.assembler import Assembler
from YAMS.instructions import InstructionMemory

with open("asm/simple_arithmetic.s") as f:
    parser = Parser(f.read())
    d, t = parser.parse()
    assembler = Assembler(t, d)
    assembler.assemble()
    print("AFTER ASSEMBLING")
    print(assembler.text_segment)

    im = InstructionMemory()
    im.load_instructions(assembler.text_segment)

    for addr, op in im._instruction_memory.items():
        print(f"{hex(addr)} - {op}")

