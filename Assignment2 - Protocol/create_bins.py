import struct

# We create the test files with invented data
with open('db1.bin', 'wb') as file:
    file.write(struct.pack('c 9s i', b'*', b'692155567', 22))

with open('db2.bin', 'wb') as file:
    file.write(struct.pack('i f ?', 22, 11.11, True))

with open('db3.bin', 'wb') as file:
    file.write(struct.pack('? 9s c', False, b'222222222', b'!'))

with open('db4.bin', 'wb') as file:
    file.write(struct.pack('i c f', 37, b'H', 22.22))

print(".bin files successfully generated.")    