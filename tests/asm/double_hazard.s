.text
.globl main
main:
    addi $1, $0, 1
    addi $3, $0, 3
    sub $2, $1, $0
    and $4, $2, $3
    or $4, $4, $2
    add $9, $4, $2