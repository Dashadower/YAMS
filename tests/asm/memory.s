.data 0x10000000
d1:
    .word 0xffffffff
d2:
    .word 0x1234ffff
.globl main
.text
main:
    la $4, d1
    la $5, d2
    lh $6, 2($5)
    or $2, $0, $0