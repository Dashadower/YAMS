# YAMS, a MIPS Simulator
~~Yet another MIPS Simulator~~

This is a MIPS simulator that implements a subset of the instruction set.

QGraphicsScene

## Installation

- For non-apple devices, just install the packages in `requirements.txt`

### Installing for apple silicon macs

- run `brew install qt`
- after installation, use `brew --prefix qt` to find the qt5 binary directory. Mine says `/opt/homebrew/opt/qt`, but the real directory is `/opt/homebrew/opt/qt@5/bin`
- add that directory to path before using pip (`export PATH="/opt/homebrew/opt/qt@5/bin:$PATH"`)
- Install `pyqt5-sip` first
- Install pyqt5 using `pip3 install pyqt5 --config-settings --confirm-license= --verbose`

https://stackoverflow.com/a/73305306/2959990

https://stackoverflow.com/a/74071222/2959990


## Pseudoinstruction support
- `li rdest, immediate`: load 32-bit `immediate` value into register `rdest`
- `la rdest, label`: load address of data label `label` into register `rdest`
- `lw rdest, label`: load word data in label `label` into register `rdest`
- `sw rdest, label`: store word data in register `rdest` into data address pointed by label `label`  