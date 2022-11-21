
## Pipeline Components

### IF
- PC Counter `PCCounter`
  - Keeps track of the current program counter
  - rising edge: value of `PCSrcMUX` if `Hazard.PCWrite` == 1 else value does not change
- PC + 4 Adder `PC4Adder`
  - computes `PC + 4`
  - update: value of `PCCounter` + 4
- Instruction Memory `InstructionMemory`
  - Fetches instruction from PC
  - update: if `IF.Flush == 1`, return `NOP`, else return instruction at `PCCounter.value`
- PC/Branch MUX `PCSrcMUX`
  - determines whether PC comes from branch target or PC + 4
  - update: if `MEM.BranchAND == 1` then value is `EXMEMRegister.BranchAddress` else `IF.PC4Adder.value`

### IF/ID Register
- PC
- Instruction
### ID
- Hazard Detection Unit `HazardDetector`
  - update: if read after write hazard is detected set `PCWrite, IF/IDWrite, Control/Zero MUX` to 0, else set all to 1
- Control `Control`
  - update: Return all control signals given instruction in `IF/IDRegister.instruction`
- Control/Zero Mux `ControlZeroMUX`
  - update: if MUX value is 0, return 0 for all control signals, else forward `Control`'s signals.
- Branch, PC Adder `BranchPCAdder`
  - update: calculate `IF/IDRegister.PC` + `ImmediateSLL2.value`
- Immediate shift left 2 `ImmediateSLL2`
  - update: calculate `ImmediateSignExtender.value << 2`
- Immediate sign extender `ImmediateSignExtender`
  - update: get immediate value from `IF/IDRegister.instruction`
- Main register `MainRegister`
  - rising edge:
    - If `RegWrite == 1` then write value of `MemtoReg` to register `RegDst`
- Branch target compare equal `BranchEqualCMP`
  - update: compute `MainRegister.ReadValue1 == MainRegister.Readvalue2`
- Branch Equal AND: `BranchEqualAND`
  - update: set `IF.Flush` to `Control.Branch AND BranchEqualCMP.value`

### ID/EX Register

### EX
- ForwardA MUX
  - update: see forward MUX documentations
- ForwardB/ALUSrc MUX
  - update: see forward MUX documentations
- ALU Control
  - given `ID/EXRegister.Funct` and `Control.ALUOp`, return ALU operation code
- ALU
  - given `ForwardA.value`, `ForwardB.value`, and `ALUControl.value` compute `zero` and `result`
- Forwarding unit
  - update: given `ID/EXRegister.rs, ID/EXRegister.rt, , EX/MEMRegister.rd` return `ForwardA.value` and `ForwardB.value`
- RegDst MUX (Rt/Rd register write location)
  - update: given `Control.RegDst, ID/EXRegister.rt, ID/EXRegister.rd`, return value selected by `Control.RegDst`

### EX/MEM Register

### MEM
- Memory
  - rising edge: If `EX/MEMRegister.MemWrite == 1`, write `EX/MEMRegister.ReadData` into address `EX/MEMRegister.ALUResult`
### MEM/WB Register

### WB



## Order of updating components
1. WriteBack WB to Main Register if `RegWrite`
2. Write data to memory if `MemWrite`
3. Update Pipeline Registers
4. Update Forwarding Unit
5. Update components in EX stage
6. Update ID Stage
   1. Update all components except for hazard detector
   2. Update Hazard Controller, which overwrites some signals
7. Update IF stage