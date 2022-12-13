
def decimal2bin(n: int) -> str:
    """
    Given a decimal number n, return its binary form as a string, without its 0x prefix
    """

    return bin(n)[2:]

def string_numeric_to_decimal(n: str) -> int:
    """
    Given a string of a numeric in either decimal or hex format, return a *decimal* integer
    """
    if n.startswith("0x"):
        return int(n, 16)
    else:
        return int(n)

def string_numeric_to_hex(n_str: str) -> str:
    """
    Given a string of a numeric in either decimal or hex format, return a "hexadecimal" integer
    """
    if n_str.startswith("0x"):
        return n_str
    else:
        return hex(n_str)


def multiple4_geq(x: int) -> int:
    """
    return the smallest multiple of 4 that's greater or equal than x
    """
    return x + 4 - (x % 4) if x % 4 != 0 else x


def zero_extend_hex(n_str: str, bytes=1, pad="0"):
    """
    given a string representation of an arbitrary number, normalize to a byte=length hex number and return as string
    """
    hex_number_string = str(hex(string_numeric_to_decimal(n_str))).split("x")[1].rjust(bytes * 2, pad)
    return "0x" + hex_number_string


def zero_extend_hex_to_word(n_str: str, pad="0") -> str:
    """
    given a string representation of an arbitrary number, normalize to a 4-byte hex number and return as string
    """
    hex_number_string = str(hex(string_numeric_to_decimal(n_str))).split("x")[1].rjust(8, pad)
    return "0x" + hex_number_string

def zero_extend_binary(n_str: str, bits=6, pad="0") -> str:
    """
    given a string representation of a binary number, normalize to a bit-length binary number and return as string
    """
    return n_str.rjust(bits, pad)


def signed_bits_to_int(bin: str) -> int:
    """
    convert a signed binary-bitstring to integer
    """
    x = int(bin, 2)
    if bin[0] == '1': # "sign bit", big-endian
       x -= 2**len(bin)
    return x

def int_to_signed_bits(number: int, n_bits=32) -> str:
    """
    convert a integer into a signed binary number of length n_bits, with the 0-th bit representing the sign bit
    """
    mask = "1" * n_bits
    result = bin(number & int(mask, 2))[2:]
    if len(result) < n_bits:
        result = zero_extend_binary(result, n_bits)

    return result

# def signed_32bits_to_hex(bin: str, bytes=4) -> str:
#     assert len(bin) == 32, "Must be a 32-bit length binary number"
#     if bin[0] == 1:
#         pad = "1"
#     else:
#         pad = "0"
#
#     result = hex(signed_bits_to_int(bin))[2:].rjust(bytes * 2,pad)
#     return "0x" + result

def signed_32bit_int2int(signed: int):
    return signed_bits_to_int(zero_extend_binary(decimal2bin(signed), bits=32))

def int2_signed_32bit_int(number: int):
    return int(int_to_signed_bits(number), 2)