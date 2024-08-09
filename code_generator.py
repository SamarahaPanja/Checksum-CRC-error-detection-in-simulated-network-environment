def generate_checksum(data):
    checksum = 0
    max_word_length = 16

    # Process the data in chunks of 16 bits
    for i in range(0, len(data), max_word_length):
        word = data[i:i+max_word_length]
        word = int(word, 2)

        # Add word to checksum
        checksum += word

        # Handle carry if any
        while (checksum >> max_word_length) > 0:
            carry = checksum >> max_word_length
            checksum = (checksum & 0xFFFF) + carry

    # One's complement of checksum
    checksum = ~checksum & 0xFFFF
    return format(checksum, '016b')

def generate_crc(data, polynomial):
    data = list(map(int, data))
    poly = list(map(int, polynomial))
    l_poly = len(poly)
    data += [0] * (l_poly - 1)
    for i in range(len(data) - l_poly + 1):
        if data[i] == 1:
            for j in range(l_poly):
                data[i + j] ^= poly[j]
    return ''.join(map(str, data[-(l_poly - 1):]))