.text
.globl main
main:
    addi $1, $0, 1
    addi $2, $0, 2
    addi $3, $0, 3
    addi $4, $0, 4
    addi $5, $0, 5
    addi $6, $0, 6
    addi $7, $0, 7
    addi $8, $0, 8
    addi $9, $0, 9
    addi $10, $0, 10
    addi $11, $0, 11
    addi $12, $0, 12
    addi $13, $0, 13
    addi $14, $0, 14
    addi $15, $0, 15

    sub $2, $1, $3
    and $12, $2, $5
    or $13, $6, $2
    add $14, $2, $2
    sw $15, 100($2)