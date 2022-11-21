.data 0x10000000
d1:
    .half 0xf
d2:
    .word 0x1234ffff
.globl main
.text
main:
    la $4, d1
    la $5, d2
    lh $6, 2($5)
    ori $2, $0, 1