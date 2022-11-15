# YAMS
Yet Another MIPS Simulator


## Installation

- For non-apple devices, just install packages in `requirements.txt`

### Installing for apple sillicon macs

- run `brew install qt`
- after installation, use `brew --prefix qt` to find the qt5 binary directory. Mine says `/opt/homebrew/opt/qt`, but the real directory is `/opt/homebrew/opt/qt@5/bin`
- add that directory to path before using pip (`export PATH="/opt/homebrew/opt/qt@5/bin:$PATH"`)
- Install `pyqt5-sip` first
- Install pyqt5 using `pip3 install pyqt5 --config-settings --confirm-license= --verbose`

https://stackoverflow.com/a/73305306/2959990