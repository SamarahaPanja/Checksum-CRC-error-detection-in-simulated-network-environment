from code_generator import *

CRC_POLYNOMIALS = {
    "CRC-8": "111010101",
    "CRC-10": "11011000101",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111"
}

def xor(a, b):
    """
    Perform XOR operation between two binary strings
    """
    result = []
    for i in range(1, len(b)):
        result.append('0' if a[i] == b[i] else '1')
    return ''.join(result)

def mod2div(dividend, divisor):
    """
    Perform binary division (modulo 2) between dividend and divisor
    """
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]
        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword

def check_checksum(chunks, checksum):
    res = 0  # Initialize result as an integer for summing
    size = len(chunks[0])

    for chunk in chunks:
        if chunk == '':
            continue
        res += int(chunk, 2)  # Add binary chunks as integers

    # Add the checksum
    res += int(checksum, 2)

    res_bin = bin(res)  # Convert result back to binary string
    res_bin = res_bin[2:]  # Remove '0b' prefix
    res_bin = res_bin.zfill(size)

    # Handle carry bits
    while len(res_bin) > size:
        carry = res_bin[:-size]
        res_bin = res_bin[-size:]
        res_bin = bin(int(res_bin, 2) + int(carry, 2))[2:].zfill(size)

    # Check if the result is all 1s
    return all(bit == '1' for bit in res_bin)

def validate_checksum_codeword(codeword):
    # Split the codeword into 16-bit chunks, excluding the last 16 bits for checksum
    padded_codeword = codeword[:-16].ljust((len(codeword) - 16 + 15) // 16 * 16, '0')
    chunks = [padded_codeword[i:i+16] for i in range(0, len(padded_codeword), 16)]
    checksum = codeword[-16:]
    return check_checksum(chunks, checksum)

def validate_crc_codeword(codeword, crc_type):
    """
    Validates a codeword with CRC for the given dataword using the specified CRC type.

    Args:
    - codeword (str): The received codeword as a string of '0's and '1's.
    - crc_type (str): The CRC type ('CRC-8', 'CRC-10', 'CRC-16', 'CRC-32').

    Returns:
    - bool: True if the codeword is valid (no errors detected), False otherwise.
    """
    polynomial = CRC_POLYNOMIALS[crc_type]
    l_key = len(polynomial)

    remainder = mod2div(codeword, polynomial)
    return remainder.count('1') == 0