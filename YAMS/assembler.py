from dataclasses import dataclass, field
from .parser import TextSegment, DataSegment
from .utils import multiple4_geq, string_numeric_to_decimal, zero_extend_hex_to_word
from typing import Dict
import re

register_name_pattern = re.compile(r"\$[a-z\d]+")

register_indices = {
    "$zero": 0,
    "$at": 1,
    "$v0": 2,
    "$v1": 3,
    "$a0": 4,
    "$a1": 5,
    "$a2": 6,
    "$a3": 7,
    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 15,
    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23,
    "$t8": 24,
    "$t9": 25,
    "$k0": 26,
    "$k1": 27,
    "$gp": 28,
    "$sp": 29,
    "$fp": 30,
    "$ra": 31
}


class Assembler:
    def __init__(self, text_segment: TextSegment, data_segment: DataSegment):
        self.text_segment = text_segment
        self.data_segment = data_segment

        # The symbol table holds the offset of data, relative to the data start address of data labels
        self.data_symbol_table: Dict[str, int] = {}

        # The instruction address table holds the absolute address of labeled instructions
        self.instruction_address_table: Dict[str, int] = {}

    def assemble(self):
        # 1. Process data labels
        # The assembler doesn't actually "allocate", but only calculates the data offset for each label

        current_data_write_offset = 0
        for entry in self.data_segment.iter_entries():
            if entry.label:
                self.data_symbol_table[entry.label] = current_data_write_offset

            if entry.type == ".ascii":
                # Make sure we're writing to byte-address (address is multiple of 4)
                current_data_write_offset = multiple4_geq(current_data_write_offset)

                current_data_write_offset += len(entry.content) * 4

            elif entry.type == ".asciiz":
                # Make sure we're writing to byte-address (address is multiple of 4)
                current_data_write_offset = multiple4_geq(current_data_write_offset)

                # .asciiz inserts \0 to the end of the string
                current_data_write_offset += len(entry.content) * 4 + 4

            elif entry.type == ".byte":
                # .byte writes 1 byte to memory
                current_data_write_offset += 1

            elif entry.type == "half":
                # .half writes 16 bits to memory
                current_data_write_offset += 2

            elif entry.type == ".space":
                # .space writes n bytes to memory
                current_data_write_offset += int(entry.content)

            elif entry.type == ".word":
                current_data_write_offset += 4

        # 2. Assemble pseudo-instructions and resolve labels
        # The assembler will resolve any label usage and/or pseudo-instructions
        # It will continually run the assembly process until a fixed point is reached, which then it will terminate
        current_text_segment = self.text_segment
        n_iterations = 0
        max_iterations = len(list(current_text_segment.iter_entries())) * 3
        while True:
            if n_iterations > max_iterations:
                raise Exception(f"Assembly failed - failed to reached a fixed point even after running {max_iterations} times. Please check that your code is correct.")
            self.instruction_address_table = {}
            new_text_segment = self._assemble_pseudo(current_text_segment)
            new_text_segment = self._substitute_labels(new_text_segment)
            new_text_segment = self._substitute_register_names(new_text_segment)

            if new_text_segment == current_text_segment:
                break

            current_text_segment = new_text_segment
            n_iterations += 1

        self.text_segment = new_text_segment


    def _assemble_pseudo(self, text_segment) -> TextSegment:
        """
        Processes pseudo-instructions. This will create a new TextSegment that assembles the pseudoinstructions.
        """

        new_ts = TextSegment()

        current_instruction_addr = text_segment.starting_address

        for instruction in text_segment.iter_entries():
            if instruction.label:
                new_ts.set_label(instruction.label)
                self.instruction_address_table[instruction.label] = current_instruction_addr

            new_ts.set_assembler_remark(instruction.assembler_remark)

            if instruction.instruction == "li":
                # li pseudoinstruction - load argument into target register
                # This is assembled into: li -> lui, ori
                target_register, immediate = instruction.arguments
                hex_number_string = str(hex(string_numeric_to_decimal(immediate))).split("x")[1].rjust(8, "0")

                immediate = string_numeric_to_decimal(immediate)  # decimal int of immediate
                ori_source_register = "$0"
                if immediate > 0xfff:  # if number is bigger than 0xfff, do lui first
                    new_ts.insert(instruction="lui", arguments=["$at", f"0x{hex_number_string[0:4]}"], original_text=f"lui $1, {f'0x{hex_number_string[0:4]}'}")
                    ori_source_register = "$at"
                    current_instruction_addr += 4

                if (immediate & 0x0000ffff) != 0:
                    new_ts.insert(instruction="ori", arguments=[target_register, ori_source_register, f"0x{hex_number_string[-4:]}"], original_text=f"ori {target_register}, {ori_source_register}, {f'0x{hex_number_string[-4:]}'}")
                else:
                    new_ts.insert(instruction="or", arguments=[target_register, ori_source_register, "$0"], original_text=f"ori {target_register}, {ori_source_register}, {f'0x{hex_number_string[-4:]}'}")
                current_instruction_addr += 4

            elif instruction.instruction == "la":
                # la pseudo-instruction (la target, address) - load address into target register
                # This is assembled into: la -> li -> lui, ori
                target_register, address = instruction.arguments
                if address in self.data_symbol_table:
                    address = str(self.data_symbol_table[address] + self.data_segment.starting_address)

                new_ts.insert(instruction="li", arguments=[target_register, address], original_text=instruction.original_text)
                current_instruction_addr += 4

            elif instruction.instruction == "nop":
                # NOP
                # this is assembled into sll $0, $0, 0
                new_ts.insert(instruction="sll", arguments=["$0","$0", "0"], original_text="sll $0, $0, 0")
                current_instruction_addr += 4

            else:
                new_ts.insert(instruction=instruction.instruction, arguments=instruction.arguments, original_text=instruction.original_text)
                current_instruction_addr += 4

        return new_ts

    def _substitute_labels(self, text_segment) -> TextSegment:
        """
        This procedure substitutes in address in place of labels

        For data labels in load/store instructions, calculate offset
        For jump label instructions, calculate jump address and substitute
        """
        new_ts = TextSegment()

        current_instruction_addr = text_segment.starting_address

        for instruction in text_segment.iter_entries():
            if instruction.label:
                new_ts.set_label(instruction.label)

            new_ts.set_assembler_remark(instruction.assembler_remark)

            if instruction.instruction in ("lw", "sw") and instruction.arguments[1] in self.data_symbol_table:
                # lw/sw with label usage (sw $5, label)
                # This is assembled into: la, lw/sw -> li, lw/sw -> lui, ori, lw/sw
                target_register = instruction.arguments[0]
                new_ts.insert(instruction="la", arguments=["$at", instruction.arguments[1]], original_text=instruction.original_text)
                current_instruction_addr += 4
                new_ts.insert(instruction=instruction.instruction, arguments=[target_register, f"0($at)"], original_text=instruction.original_text)
                current_instruction_addr += 4

            elif instruction.instruction == "j" and instruction.arguments[0] in self.instruction_address_table:
                # j label instruction
                # Substitute address instead of label
                jump_addr = hex(int(self.instruction_address_table[instruction.arguments[0]] / 4))
                new_ts.insert(instruction=instruction.instruction, arguments=[jump_addr], original_text=instruction.original_text)
                current_instruction_addr += 4

            elif instruction.instruction == "beq" and instruction.arguments[2] in self.instruction_address_table:
                # beq label instruction
                # substitute address instead of label
                # beq address is offset between target and PC + 4. So if branch target is the next instruction, it's 0
                # and if it's the 2nd instruction after, then it's 4
                jump_addr = self.instruction_address_table[instruction.arguments[2]]
                branch_addr = (jump_addr - (current_instruction_addr + 4)) // 4
                new_ts.insert(instruction=instruction.instruction, arguments=[instruction.arguments[0], instruction.arguments[1], str(branch_addr)], original_text=instruction.original_text)
                current_instruction_addr += 4

            else:
                new_ts.insert(instruction=instruction.instruction, arguments=instruction.arguments, original_text=instruction.original_text)
                current_instruction_addr += 4

        return new_ts

    def _substitute_register_names(self, text_segment):
        new_ts = TextSegment()

        current_instruction_addr = text_segment.starting_address

        for instruction in text_segment.iter_entries():
            if instruction.label:
                new_ts.set_label(instruction.label)

            new_ts.set_assembler_remark(instruction.assembler_remark)

            new_argument_list = []
            for argument in instruction.arguments:
                register_names = list(register_name_pattern.findall(argument))
                assert len(register_names) <= 1, f"Error while assembling instruction - Each argument of instruction must contain at most 1 register: {instruction}"
                if not register_names:
                    new_argument_list.append(argument)
                else:
                    register_name: str = register_names[0]
                    if register_name in register_indices:
                        new_argument_list.append(argument.replace(register_name, f"${register_indices[register_name]}"))
                    else:
                        register_index = register_name.split("$")[1]
                        assert register_index.isnumeric(), f"Error while assembling instruction {instruction} - Unknown register {register_name}"
                        assert 0 <= int(register_index) <= 31, f"Error while assembling instruction {instruction} - Register ${register_index} is out of bounds."
                        new_argument_list.append(argument)

            new_ts.insert(instruction=instruction.instruction, arguments=new_argument_list, original_text=instruction.original_text)
            current_instruction_addr += 4

        return new_ts


    def repr_instructions(self) -> str:
        ret = ""
        current_instruction_addr = self.text_segment.starting_address
        for instruction in self.text_segment.iter_entries():
            comment = ""
            if instruction.label:
                comment += f"{instruction.label}: "
            if instruction.assembler_remark:
                comment += instruction.assembler_remark

            if comment:
                comment = "# " + comment
            ret += f"[{zero_extend_hex_to_word(hex(current_instruction_addr))}]     {instruction.instruction} {', '.join(instruction.arguments)}".ljust(50) + comment + "\n"
            current_instruction_addr += 4

        return ret




