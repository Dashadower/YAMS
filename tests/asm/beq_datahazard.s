.text
.globl main
main:
    addi $t0, $t0, 10
    addi $t2, $0, 10
    beq $t2, $t0, main
