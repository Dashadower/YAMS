.text
.globl main
main:
    addi $1, $0, 1
    addi $3, $0, 3
    sub $2, $1, $0
    and $4, $2, $3  # Hazard : 1 & 3 = 001 & 011 = 1
    or $4, $4, $2   # Hazard : 1 | 1 = 1
    add $9, $4, $2  # Hazard : 1 + 1 = 2