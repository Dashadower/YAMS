.data
    .word 12345
    .word 0xffffffff
	message: .asciiz "Hello World! \n"
.text
	main: li $v0, 4
		la $a0, message
		syscall

        lw $2, 0x10010002

		li $v0, 10
		syscall
