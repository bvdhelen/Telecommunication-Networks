#Elena Sol Díaz Contreras
#Assignment2 - Protocol

# Task1
# Read the binary files received in the parameter and print the contents of the first record to the standard output! (the return value of the unpack)
    # Parameter1 structure: char, 9 length string, integer
        # struct -> [c 9s i]
    # Parameter2 structure: integer, float, bool
        # struct -> [i f ?]
    # Parameter3 structure: bool, 9 length string, char
        # struct -> [? 9s c]
    # Parameter4 structure: integer, char, float
        # struct -> [i c f]

# Task2
# Write the following value to stdout (print) in binary format (the return value of the pack)! The length of the string is indicated by the number behind the text!
# Struct parameter to use: f, i, c, ?, Xs (where X is the length of the string, eg: 3s)
    # "elso"(19), 49, True
        # struct -> [19s i ?]
    # 52.5, False, 'X'
        # struct -> [f ? c]
    # 40, "masodik"(17), 59.9
        # struct -> [i 17s f]
    # 'Z', 71, "harmadik"(20)
        # struct -> [c i 20s]

import struct
import sys

def main():
    
    if len(sys.argv) < 5:
        print("Usage example: py .\\client.py <db1.bin> <db2.bin> <db3.bin> <db4.bin>")
        sys.exit(1)
    
    # Task1
    # We define the structures and their corresponding sizes
    formats = [
        'c 9s i', #Param 1
        'i f ?', #Param 2
        '? 9s c', #Param 3
        'i c f' #Param 4
    ]

    # We iterate over the 4 files passed as parameters
    for i in range(1, 5):
        file_path = sys.argv[i]
        fmt = formats[i-1]

        try:
            with open(file_path, 'rb') as file:
                # We calculate how many bytes we need to read based on the structure
                size = struct.calcsize(fmt)
                data = file.read(size)

                if len(data) == size:
                    # We unpack and print it (this prints a tuple)
                    unpacked_data = struct.unpack(fmt, data)
                    print(unpacked_data)
                else:
                    print(f"Error: The file {file_path} is empty or incomplete")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")

    # Task2
    # We pack the values ​​and output them in binary format
    # 1. "elso"(19), 49, True
    packed1 = struct.pack('19s i ?', b'elso', 49, True)
    print(packed1)

    # 2. 52.5, False, 'X'
    packed2 = struct.pack('f ? c', 52.5, False, b'X')
    print(packed2)

    # 3. 40, "masodik"(17), 59.9
    packed3 = struct.pack('i 17s f', 40, b'masodik', 59.9)
    print(packed3)

    # 4. 'Z', 71, "harmadik"(20)
    packed4 = struct.pack('c i 20s', b'Z', 71, b'harmadik')
    print(packed4)

if __name__ == "__main__":
    main()

# Submission:
    # Send it to the TMS in .zip file which should contain one and only one file called client.py!
