from typing import Dict, List, Any, Tuple, Union
from dataclasses import dataclass, field
from collections import OrderedDict
import re

comment_removed = re.compile("^.*?(?=#|$)")  # capture all characters before first '#'

@dataclass
class DataEntry:
    type: str
    content: str
    label: str = field(default=None)

    def __str__(self):
        return f"<DataEntry({self.label}, {self.type}) - {self.content}>"


@dataclass
class TextEntry:
    content: str
    label: str = field(default=None)

    def __str__(self):
        return f"<TextEntry({self.label}) - {self.content}>"


class DataSegment:
    def __init__(self):
        self.starting_address = None
        self._labels: List[DataEntry] = []
        self._current_label = None

    def insert(self, data_type: str, content: str):
        if not self._current_label:
            self._labels.append(DataEntry(data_type, content))
        else:
            self._labels.append(DataEntry(data_type, content, label=self._current_label))
            self._current_label = None

    def set_label(self, label_name: str):
        if label_name in self._labels:
            raise Exception(f"Data segment label {label_name} already exists but is being reused!!")

        self._current_label = label_name

    def __str__(self):
        ret = ""
        ret += f"<DataSegment(addr={self.starting_address})>\n"
        for entry in self._labels:
            ret += f"    {entry}\n"
        return ret


class TextSegment:
    def __init__(self):
        self.starting_address = None
        self._labels: List[TextEntry] = []
        self._current_label = None

    def insert(self, content: str):
        if not self._current_label:
            self._labels.append(TextEntry(content))
        else:
            self._labels.append(TextEntry(content, label=self._current_label))
            self._current_label = None

    def set_label(self, label_name: str):
        if label_name in self._labels:
            raise Exception(f"Text segment label {label_name} already exists but is being reused!!")

        self._current_label = label_name

    def __str__(self):
        ret = ""
        ret += f"<TextSegment(addr={self.starting_address})>\n"
        for entry in self._labels:
            ret += f"    {entry}\n"
        return ret

def preprocess(program_text: str) -> List[str]:
    separated_lines = []
    for line in program_text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # 1. Remove any comments (# comment strings)
        line = comment_removed.findall(line)[0]

        # 2. Separate lines where identifiers (e.g: main:) are on the same line as code.
        #    For example, `main: addi $2, $0, 1` would be separated into `main:` and `addi $2, $0, 1`
        tokens = line.split(" ")
        if tokens[0].endswith(":"):  # check if the first word of the line is an identifier
            segments = line.split(":")
            if len(segments) > 1:  # If they are written on the same line, separate them
                separated_lines.append(tokens[0])
                separated_lines.append(" ".join(tokens[1:]))
                continue

        separated_lines.append(line)

    return separated_lines


class Parser:
    """
    The Parser is a 3-state state machine.

    - Initial state: only allows `.data`, `.text`, and `.globl` directives.
        - Entry: before reading any lines, immediately after parser initialization
        - Transitions:
            - Data state: when `.data` directive is observed
            - Text state: when `.text` directive is observed

    - Data state: Allows (un)labeled data declarations through directives.
        - Entry: By state transition from another state
        - Transitions:
            - Text state: when `.text` directive is observed

    - Text state: Allows (unlabeled) arbitrary command declarations.
        - Entry: By state transition from another state
        - Transitions:
            - Data state: when `.data` directive is observed
    """
    def __init__(self, program_text):
        self.program_lines = preprocess(program_text)
        self.line_index = 0  # line index to retrieve next

        # These two classes hold the results of the parsed program
        self.data_segment = DataSegment()
        self.text_segment = TextSegment()

        # This attribute holds the current executing state of the parser state machine
        self.current_state = self.initialization_state

    def get_next_line(self):
        if self.line_index < len(self.program_lines):
            line = self.program_lines[self.line_index]
            self.line_index += 1
            return line

        return ""

    def parse(self):
        """
        This should be the entry point of the parser
        """
        while self.program_lines:
            line = self.program_lines.pop(0)
            self.current_state(line)

        return self.data_segment, self.text_segment

    def initialization_state(self, line: str):
        if not line:
            return

        tokens = line.split()
        n_tokens = len(tokens)
        head = tokens[0]

        if head == ".data":
            if n_tokens == 2:  # .data <addr> is specified
                self.data_segment.starting_address = head[1]
            self.current_state = self.data_state
        elif head == ".text":
            if n_tokens == 2:  # .data <addr> is specified
                self.text_segment.starting_address = head[1]
            self.current_state = self.text_state
        elif head == ".globl":
            pass
        else:
            raise Exception(f"Assembly file did not define a .data or .text segment and instead called '{head}' first.")

    def data_state(self, line: str):
        if not line:
            return

        tokens = line.split()
        n_tokens = len(tokens)
        head = tokens[0]

        if head.endswith(":"):  # label:
            # Label is defined. Set label as the text up to, but not including the column
            self.data_segment.set_label(head[:-1])

        elif head == ".text":
            if n_tokens == 2:  # .data <addr> is specified
                self.text_segment.starting_address = head[1]
            self.current_state = self.text_state

        elif head == ".globl":
            pass

        else:
            allowed_data_types = [".ascii", ".asciiz", ".double", ".float", ".word"]
            if head not in allowed_data_types:
                raise Exception(f"Assembler directive '{head}' used within data segment, is unknown.")

            data = " ".join(tokens[1:])
            if head in (".ascii", ".asciiz"):
                # ascii text is defined as `.ascii "This is my string"`
                # Parse the data that's between the double quotation marks
                dblquote_indices = [i for i, x in enumerate(data) if x == '"']
                assert len(dblquote_indices) >= 2, "'.ascii' must be defined as a string using double quotation marks."
                data = data[(dblquote_indices[0] + 1):(dblquote_indices[-1])]

            self.data_segment.insert(head, data)

    def text_state(self, line: str):
        if not line:
            return

        tokens = line.split()
        n_tokens = len(tokens)
        head = tokens[0]

        if head.endswith(":"):  # label:
            # Label is defined. Set label as the text up to, but not including the column
            self.text_segment.set_label(head[:-1])

        elif head == ".data":
            if n_tokens == 2:  # .data <addr> is specified
                self.data_segment.starting_address = head[1]
            self.current_state = self.data_state

        elif head == ".globl":  # global declarations can be ignored for now
            pass

        else:
            self.text_segment.insert(" ".join(tokens))