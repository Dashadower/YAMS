.data
m: .word 0x12345678
.text
.globl main
main:
    addi $t1, $t1, 1
    sw $t1, 0($sp)
    addi $sp, $sp, -4
    lw $t2, 4($sp)
    add $t3, $t2, $0

    beq $t2, $t1, main
