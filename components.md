
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
  - update: if `ID.BranchEqualAND.(IF.Flush) == 1`, return `NOP`, else return instruction at `PCCounter.value`
- PC/Branch MUX `PCSrcMUX`
  - determines whether PC comes from branch target or PC + 4
  - update: if `ID.BranchEqualAND == 1` then value is `ID.BranchPCAdder` else if `Control.Jump` then value is `JaddrCalc.value` else  `IF.PC4Adder.value`

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
- Set Control to zero OR `ControlZeroSetOR`
  - update: value is `Hazard.IDFlush | instruction is NOP`
- Branch, PC Adder `BranchPCAdder`
  - update: calculate `IF/IDRegister.PC` + `ImmediateSLL2.value`
- Immediate shift left 2 `ImmediateSLL2`
  - update: calculate `ImmediateSignExtender.value << 2`
- Immediate sign extender `ImmediateSignExtender`
  - update: get immediate value from `IF/IDRegister.instruction`
- Main register `MainRegister`
  - rising edge: If `RegWrite == 1` then write value of `MemtoReg` to register `RegDst`s
- Branch target compare equal `BranchEqualCMP`
  - update: compute `MainRegister.ReadValue1 == MainRegister.Readvalue2`
- Branch target compare ForwardA MUX `BranchCMPForwardAMUX`
  - register read value
  - value of ALU
  - value of memory read
- Branch target compare ForwardB MUX `BranchCMPForwardBMUX`
  - register read value
  - value of ALU
  - value of memory read
- Branch Equal AND: `BranchEqualAND`
  - update: set `IF.Flush` to `Control.Branch AND BranchEqualCMP.value`
- PCUpper4bitSelector `PCUpper4bitSelector`
  - Selects the upper 4 bits of PC + 4 (`IF/IDRegister.PC`[31~28])
- Jump address shift left 2 `JaddrSLL2`
  - Selects [25~0] bits of the `IF/IDRegister.instruction`(jformat), performs shift left 2 bits
- Jump address calculate `JaddrCalc`
  - Calculates jump address `f"0b{PCUpper4bitSelector.value}{JaddrSLL2.value}00"`

### ID/EX Register

### EX
- ForwardA MUX `ForwardAMUX`
  - update: see forward MUX documentations
- ForwardB/ALUSrc MUX `ForwardBMUX`
  - update: see forward MUX documentations
- ALUSrc MUX `ALUSrcMUX`
  - second operand of ALU is from `ID/EXRegister.Immediate` or `ForwardBMUX`
- ALU Control `ALUControl`
  - given `ID/EXRegister.Funct` and `Control.ALUOp`, return ALU operation code
- ALU `ALU`
  - given `ForwardA.value`, `ForwardB.value`, and `ALUControl.value` compute `zero` and `result`
- Forwarding unit `ForwardingUnit`
  - update: given `ID/EXRegister.rs, ID/EXRegister.rt, , EX/MEMRegister.rd` return `ForwardA.value` and `ForwardB.value`
- RegDst MUX (Rt/Rd register write location) `RegDstMUX`
  - update: given `Control.RegDst, ID/EXRegister.rt, ID/EXRegister.rd`, return value selected by `Control.RegDst`

### EX/MEM Register

### MEM
- Memory `Memory`
  - rising edge: If `EX/MEMRegister.MemWrite == 1`, write `EX/MEMRegister.ReadData` into address `EX/MEMRegister.ALUResult`
### MEM/WB Register

### WB
- Mem2Reg MUX `Mem2RegMUX`
  - update: If `MEM/WBRegister.Mem2Reg == 0` set `MEM/WBRegister.ALUResult`, elif `MEM/WBRegister.Mem2Reg == 1` set `Memory.ReadData`

  
## Order of updating components
1. WriteBack WB to Main Register if `RegWrite`
2. Write data to memory if `MemWrite`
3. Update Pipeline Registers
4. Update Forwarding Unit
5. Update ALU control
5. Update components in EX stage
6. Update ID Stage
   1. Update all components except for hazard detector
   2. Update Hazard Controller, which overwrites some signals
7. Update IF stage


## Sharp bits
- load-use hazard for beq requires *2 stalls*. (`lw $t2, 0($t1); beq $t2, $t0, main`)
- Jump address calculation is performed at ID


## Stall strategies
- load-use stall
  - after a load instruction is performed:
    - if following instruction uses target register, stall 1 cycle
      - `if IDEXRegister.control_MemRead == 1 && IDEXRegister.Rt == (IFIDRegister.Rt or IFIDRegister.Rs)`
        - set IFID to NOP and zero control signals
    - if a conditional branch instruction uses target register, stall **2** cycles
      - `if IDEXRegister.control_MemRead == 1 && IDEXRegister.Rt == (IFIDRegister.Rt or IFIDRegister.Rs) && IFIDRegister has instruction beq`
        - set IFID to successive NOP 1 (stall and stall 1 succeeding cycle) and zero control signals
- branch taken stall(flush)
  - if `BranchEqualAND == 1`, set flush to 1, which sets IF register to NOP
- special NOP
  - set IFID to NOP and zero control signals

## Stall vs Flush
- Stall - re-run the instruction because of dependency: 
  - Force write-related control signals to 0
  - Set PCWrite and IFWrite HAZARD control signals to 0
- Flush - used when branch is taken:
  - Set IF.Flush control signal to 0, which sets entire Instruction segemnt if IFID register to zero
  - Zero all the control signals
  - Update the PC to use branch address


## Special internal instruction
This instruction is used only internally for resolving lw-beq hazards
- successive NOP
  - jformat with op: 19
  - Upon decoding, stall for `immediate` cycles
  - semantically equivalent to `immediate` amount of NOPs