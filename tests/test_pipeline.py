from YAMS.pipeline import PipelineCoordinator
from YAMS.parser import Parser
from YAMS.assembler import Assembler
from YAMS.instructions import InstructionMemoryHandler
from YAMS.memory import Memory

with open("asm/simple_jump.s") as f:
    parser = Parser(f.read())
    d, t = parser.parse()
    assembler = Assembler(t, d)
    assembler.assemble()
    print("AFTER ASSEMBLING")
    print(assembler.text_segment)

    im = InstructionMemoryHandler()
    im.load_instructions(assembler.text_segment)

    for addr, op in im._instruction_memory.items():
        print(f"{hex(addr)} - {op}")

    mem = Memory(endian="little")

    mem.load_datasegment(d)

    print("#" * 5)

    pipeline = PipelineCoordinator(im, mem)
    pipeline.initialize()
    for x in range(1, 20):
        print("@@@@ Cycle", x)
        pipeline.single_step()

    print(pipeline.ID_MainRegister)

    print("MEMORY CONTENTS")

    print(mem)

