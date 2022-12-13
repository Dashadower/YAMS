.text
.globl main
main:
    addi $t0, $0, 10
    addi $t2, $0, 10
    beq $t2, $t0, main  # stall for 1 cycle, and then jump
    add $t3, $0, $0
