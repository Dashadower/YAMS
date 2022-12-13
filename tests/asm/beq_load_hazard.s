.data
m: .word 0x12345678
.text
.globl main
main:
    addi $t1, $t1, 1
    sw $t1, 0($sp)
    addi $sp, $sp, -4
    lw $t2, 4($sp)
    beq $t2, $t1, main  # stall for two cycles

# expected behavior is branch takes and program repeats indefinitely, while $t1 increases
