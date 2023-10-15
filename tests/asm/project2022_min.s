# add sub and or slt lw sw beq j (nop)

	.text
main:
		slt $t5, $t1, $t0 # 13,21,29,37,45] $t0 no forwarding, but should read an updated value from the register file
		beq $t5, $0, loop # 14,15,22,23,30,31,38,39,46,47] 1 cycle stall, then $t5 forward from EX/MEM
		                  # 16,24,32,40 ] 1 cycle stall x 4 times (branch hazard when taken)  ### ERRORS HERE

		sub $t6, $t5, $t4

loop:
    addi $t0, $0, 0


