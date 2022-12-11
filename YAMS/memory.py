from typing import TYPE_CHECKING, Dict
from .utils import string_numeric_to_decimal, zero_extend_hex_to_word, string_numeric_to_hex, zero_extend_hex, multiple4_geq
from collections import defaultdict

if TYPE_CHECKING:
    from .parser import DataSegment, DataEntry


class Memory:
    def __init__(self, endian="big"):
        self._memory: Dict[int, int] = defaultdict(lambda: 0)
        self.starting_address = None
        self.endian = endian

    def store_byte(self, addr: int, byte: int):
        """
        Store a single byte to addr
        """
        self._memory[addr] = byte

    def _input_to_int(self, data: str, ascii=False):
        if ascii:
            # convert ascii string to numeric
            hex_representation = "0x"
            for char in data:
                char_hex = zero_extend_hex(hex(ord(char)))
                hex_representation += char_hex.split("x")[1]

            return int(hex_representation, base=16)

        if data.startswith("0x"):
            # hexadecimal number
            return int(data, base=16)
        else:
            return int(data)

    def store_word(self, addr: int, data: int) -> None:
        """
        Store a single word(4 bytes) into address addr. Follows self.endian
        """
        data_hex = hex(data)
        assert len(data_hex) <= 10, f"Data size for word must be less or equal to 4 bytes but got data {data_hex}"
        data_hex_word = zero_extend_hex_to_word(data_hex).split("x")[1]  # zero extend to 4 bytes
        memory_order = [(0, 2), (2, 4), (4, 6), (6, 8)]
        if self.endian == "little":
            memory_order = reversed(memory_order)

        for addr_offset, byte_index in enumerate(memory_order):
            self.store_byte(addr + addr_offset, int(data_hex_word[byte_index[0]:byte_index[1]], base=16))

    def load_byte(self, addr: int) -> int:
        return self._memory[addr]

    def load_word(self, addr: int) -> int:
        memory_order = [(0, 2), (2, 4), (4, 6), (6, 8)]
        if self.endian == "little":
            memory_order = reversed(memory_order)

        data_hex = ["0"] * 8

        for addr_offset, byte_index in enumerate(memory_order):
            byte = self.load_byte(addr + addr_offset)
            hex_byte = zero_extend_hex(hex(byte), bytes=1).split("x")[1]
            data_hex[byte_index[0]] = hex_byte[0]
            data_hex[byte_index[0] + 1] = hex_byte[1]

        return int("".join(data_hex), 16)

    def load_datasegment(self, data_segment: "DataSegment"):
        self.starting_address = data_segment.starting_address
        current_address = self.starting_address

        for entry in data_segment.iter_entries():
            if entry.type == ".word":
                current_address = multiple4_geq(current_address)
                self.store_word(current_address, self._input_to_int(entry.content))
                current_address += 4

            elif entry.type == ".byte":
                self.store_byte(current_address, self._input_to_int(entry.content))
                current_address += 1

            elif entry.type == ".ascii":
                for char in entry.content:
                    self.store_byte(current_address, ord(char))
                    current_address += 1

            elif entry.type == ".asciiz":
                for char in entry.content:
                    self.store_byte(current_address, ord(char))
                    current_address += 1

                self.store_byte(current_address, ord("\0"))
                current_address += 1

            else:
                raise Exception(f"Unsupported data type {entry.type}")

    def __repr__(self):
        entries = [(key, val) for key, val in self._memory.items()]
        entries = sorted(entries, key=lambda x: x[0])
        ret = ""
        for key, val in entries:
            ret += f"{zero_extend_hex_to_word(hex(key))} - {zero_extend_hex(hex(val))}\n"

        return ret

    def print_wordview(self, starting_address: int, n_words = 20):
        for n in range(n_words):
            addr = starting_address + n * 4
            value = self.load_word(addr)
            print(f"{zero_extend_hex_to_word(hex(addr))} - {zero_extend_hex_to_word(hex(value))}\n")


