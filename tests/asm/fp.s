.data  0x10008000

.float 0.1, 2.1, 0.0



.text 0x00410000

.globl main

main:

    lwc1 $f4, 0($gp) 

    lwc1 $f5, 4($gp) 

    add.s $f2, $f4, $f5 

    swc1 $f2, 8($gp) 
