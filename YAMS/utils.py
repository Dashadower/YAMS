
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
    given a string representation of an arbitrary number, normalize to a bit-length binary number and return as string
    """
    return bin(string_numeric_to_decimal(n_str))[2:].rjust(bits, pad)


def signed_bits_to_int(bin: str):
    """
    convert a signed binary-bitstring to integer
    """
    x = int(bin, 2)
    if bin[0] == '1': # "sign bit", big-endian
       x -= 2**len(bin)
    return x