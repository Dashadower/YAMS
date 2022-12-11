# Component dependencies

This is for resolving the order of calling `update()` for pipeline components

- A
  - B

Implies that A is dependent on B and thus `B.update()` must be called before `A.update()`

## IF

- IF_PCSrcMux
  - ID_BranchEqualAND
  - ID_BranchPCAdder
  - ID_JaddrCalc
  - IF_PC4Adder
- IF_PCCounter
  - IF_PCSrcMUX
- IF_PC4Adder
  - IF_PCCounter
- IF_InstructionMemory
  - IF_PCCounter

## ID
- ID_MainRegister
- ID_HazardDetector
  - ID_Control
- ID_Control
- ID_ControlZeroMUX
  - ID_HazardDetector
  - ID_Control
- ID_ControlZeroSetOR
  - ID_HazardDetector
- ID_BranchPCAdder
  - ID_ImmediateSLL2
- ID_ImmediateSLL2
  - ID_ImmediateSignExtender
- ID_ImmediateSignExtender
- ID_BranchEqualCMP
  - ID_MainRegister
- ID_BranchCMPForwardAMUX
  - ID_BranchForwardingUnit
  - WB_Mem2RegMUX
- ID_BranchCMPForwardBMUX
  - ID_BranchForwardingUnit
  - WB_Mem2RegMUX
- ID_BranchForwardingUnit
- ID_BranchEqualAND
  - ID_Control
  - ID_BranchEqualCMP
- ID_PCUpper4bitSelector
- ID_JAddrSLL2
- ID_JaddrCalc
  - ID_PCUpper4bitSelector
  - ID_JAddrSLL2

## EX
- EX_ForwardingUnit
- EX_ALUSrcMUX
- EX_ForwardAMUX
  - EX_ForwardingUnit
  - EX_ALUSrcMUX
  - WB_Mem2RegMUX
- EX_ForwardBMUX
  - EX_ForwardingUnit
  - EX_ALUSrcMUX
  - WB_Mem2RegMUX
- EX_ALUControl
- EX_ALU
  - EX_ForwardAMUX
  - EX_ForwardAMUX
  - EX_ALUControl
- EX_RegDstMUX

## MEM
- MEM_MainMemory

## WB
- WB_Mem2RegMUX


# Update order
- WB_Mem2RegMUX
- ID_MainRegister
- ID_Control
- ID_HazardDetector
- ID_ControlZeroMUX
- ID_ControlZeroSetOR
- ID_ImmediateSignExtender
- ID_ImmediateSLL2
- ID_BranchForwardingUnit
- ID_BranchCMPForwardAMUX
- ID_BranchCMPForwardBMUX
- ID_BranchPCAdder
- ID_BranchEqualCMP
- ID_BranchEqualAND
- ID_PCUpper4bitSelector
- ID_JAddrSLL2
- ID_JaddrCalc
- IF_PC4Adder
- IF_PCSrcMUX
- IF_PCCounter
- IF_InstructionMemory
- EX_ForwardingUnit
- EX_ALUSrcMUX
- EX_ForwardAMUX
- EX_ForwardBMUX
- EX_ALUControl
- EX_ALU
- EX_RegDstMUX
- MEM_MainMemory
