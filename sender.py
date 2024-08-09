import socket
import sys
import random
from code_generator import generate_checksum, generate_crc


def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().strip()
    return data

def inject_single_error(data):
    data = list(data)
    pos = random.randint(0, len(data) - 1)
    data[pos] = '1' if data[pos] == '0' else '0'
    return ''.join(data)

def inject_double_error(data):
    pos1 = random.randint(0, len(data) - 1)
    pos2 = random.randint(0, len(data) - 1)
    while pos2 == pos1:
        pos2 = random.randint(0, len(data) - 1)
    data[pos1] = '1' if data[pos1] == '0' else '0'
    data[pos2] = '1' if data[pos2] == '0' else '0'
    return ''.join(data)

def inject_burst_error(data,n):
    start = random.randint(0, len(data) - 5)
    for i in range(start, start + n):
        data[i] = '1' if data[i] == '0' else '0'
    return ''.join(data)

def main():
    if len(sys.argv) != 2:
        print("Usage: python sender.py <file_path>")
        return
    
    file_path = sys.argv[1]
    dataword = read_file(file_path)
    #generating checksum codeword and injecting error
    checksum = generate_checksum(dataword)
    codeword_checksum = dataword + checksum
    codeword_checksum = inject_single_error(codeword_checksum)

    # Compute CRC (example with CRC-8)
    polynomial = '110000111'  # CRC-8 polynomial
    crc = generate_crc(dataword, polynomial)
    codeword_crc = dataword + crc
    codeword_crc = inject_single_error(codeword_crc)

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the port on which you want to connect
    port = 12345

    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    # Send the codeword
    s.sendall(codeword_checksum.encode())
    #s.sendall(codeword_crc.encode())

    # Close the connection
    s.close()

if __name__ == "__main__":
    main()
