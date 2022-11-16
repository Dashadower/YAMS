
def decimal2hex(n: int) -> str:
    """
    Given a decimal number n, return its binary form as a string, without its 0x prefix
    """

    return bin(n)[2:]

def string_numeric_to_int(n: str) -> int:
    """
    Given a string of a numeric in either decimal or hex format, return a *decimal* integer
    """
    if n.startswith("0x"):
        return int(n, 16)
    else:
        return int(n)

def multiple4_geq(x: int) -> int:
    """
    return the smallest multiple of 4 that's greater or equal than x
    """
    return x + 4 - (x % 4) if x % 4 != 0 else x


def normalize_hex_to_byte(n: str) -> str:
    """
    given a string representation of an arbitrary number, normalize to a 8-bit hex number and return as strings
    """
    hex_number_string = str(hex(string_numeric_to_int(n))).split("x")[1].rjust(8, "0")
    return "0x" + hex_number_string
