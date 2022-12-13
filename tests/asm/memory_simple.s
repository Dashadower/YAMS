.data 0x10000000
d1:
    .word 0xffffffff
d2:
    .word 0x1234ffff
.globl main
.text
main:
    #addi $t0, $0, 7
    #sw $t0, 0($gp)
    #addi $t1, $0, 5
    lw $t2, 0($gp)
    sub $t3, $t2, $t1