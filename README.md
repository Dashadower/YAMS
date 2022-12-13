# YAMS, a MIPS Simulator
~~Yet another MIPS Simulator~~

This is a MIPS simulator that implements a subset of the instruction set.

## Supported instructions
- addi
- add
- sub
- and
- or
- ori
- slt
- j
- beq
- lw
- sw

## Installation

You need the following:
- Python 3.6 or higher (for f-strings)
- PyQt5

Run `app.py` to start the application

### Installing PyQt5 for Apple silicon

- run `brew install qt`
- after installation, use `brew --prefix qt` to find the qt5 binary directory. Mine says `/opt/homebrew/opt/qt`, but the real directory is `/opt/homebrew/opt/qt@5/bin`
- add that directory to path before using pip (`export PATH="/opt/homebrew/opt/qt@5/bin:$PATH"`)
- Install `pyqt5-sip` first
- Install pyqt5 using `pip3 install pyqt5 --config-settings --confirm-license= --verbose`

references:
https://stackoverflow.com/a/73305306/2959990
https://stackoverflow.com/a/74071222/2959990


## Pseudoinstruction support

~~The YAMS assembler iteratively assembles the instructions, until a fixed point is reached. This is done by substituting
instructions(or even pseudo-instructions) inplace of pseudo-instructions, and replacing any labels with its actual
allocated address.~~

- ~~`li rdest, immediate`: load 32-bit `immediate` value into register `rdest`~~
  ~~- assembled into: `li -> lui, ori`~~
- ~~`la rdest, label`: load address of data label `label` into register `rdest`~~
  - ~~assembled into: `la -> li -> lui, ori`~~
- ~~`lw rdest, label`: load word data in label `label` into register `rdest`~~
  - ~~assembled into: `lw/sw -> li, lw/sw -> lui, ori, lw/sw`~~
- ~~`sw rdest, label`: store word data in register `rdest` into data address pointed by label `label`~~
- ~~`j label`: jump to instruction address pointed by label `label`~~