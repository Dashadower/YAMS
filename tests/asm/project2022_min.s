# add sub and or slt lw sw beq j (nop)

	.text
main:
    add $t0, $0, $gp  # 1]
		lw  $t1, 40($t0)  # 2] 16  : $t0 forward from EX/MEM
		add $t1, $t1, $t0 # 3,4] 0x10008010 : 1 cycle stall, then $t1 forward from MEM/WB
		                  # $t0 no forwarding, but should read an updated value from the register file (half cycle update)
		lw  $t2, 44($t0)  # 5] 0x00020000
		or  $t2, $gp, $t2 # 6,7] 0x10028000 : 1 cycle stall, then $t2 forward from MEM/WB
		lw  $t4, 16($t0)  # 8] 4
loop:
  	lw  $t3, 0($t0)   # 9,17,25,33,41]
		add $t0, $t0, $t4	# 10,18,26,34,42] $t4 forward from MEM/WB at cycle 10
		sw  $t3, 0($t2)   # 11,19,27,35,43] $t3 forward from MEM/WB
		add $t2, $t2, $t4 # 12,20,28,36,44]
		slt $t5, $t1, $t0 # 13,21,29,37,45] $t0 no forwarding, but should read an updated value from the register file
		beq $t5, $0, loop # 14,15,22,23,30,31,38,39,46,47] 1 cycle stall, then $t5 forward from EX/MEM
		                  # 16,24,32,40 ] 1 cycle stall x 4 times (branch hazard when taken)  ### ERRORS HERE

	  sub $t6, $t5, $t4 # 48] -3 : $t5 forward from MEM/WB
		j   jta           # 49] 1 cycle stall (branch hazard)
		and $t6, $t5, $t4 # 50] should not be executed (flushed)
	  lw  $t7, 0($gp)
jta: add $t6, $t6, $t4 # 51] 1 : $t6 no forwarding, but should read an updated value from the register file
     sub $sp, $sp, $t4 # 52] 0x7ffffe3c
		 sw  $t6, 0($sp)   # 53] $sp forward from EX/MEM, $t6 forward from MEM/WB
		 add $sp, $sp, $t4 # 54] 0x7ffffe40 : $sp forward from MEM/WB

     lw $t7, 12($gp)   # 55] 3
		 beq $t7, $0, jta  # 56,57,58] 2 cycles stall
     add $16, $0, $t4  # 59] 4
		 sub $16, $t7, $0  # 60] 3 : $t7 forward from MEM/WB
		 or  $17, $0, $16 # 61] 3 : $16 double data hazard, forward from EX/MEM
		 add $18, $0, $t4 # 62] 4
		 add $19, $0, $t7 # 63] 3
		 add $20, $0, $t6 # 64] 1

.data 0x10008000
.word 0
.word 1
.word 2
.word 3
.word 4
.word 5
.word 6
.word 7
.word 8
.word 9
.word 16
.word 0x00020000
#.byte 8
#.asciiz "xy"
#.float 0.1
