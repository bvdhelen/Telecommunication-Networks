import struct

with open("input.txt", "rb") as file:
    print(file.read())
    print(file.read(128))

print("=====")
values = (1, 'ab'.encode(), 2.7)
packer = struct.Struct('i 2s f') # Int, char[2], float
packed_data = packer.pack(*values)
print(packed_data)

unpacker = struct.Struct('i 2s f')
unpacked_data = unpacker.unpack(packed_data)
print(unpacked_data)
print(packer.size)

print("=====")

with open('input.txt', 'r') as f:
    line = f.readline()
    print('Current row:', line.strip())
    line = f.readline()
    print('Current row:', line.strip())
    f.seek(3, 0)
    line = f.readline()
    print('Current row:', line.strip())

print("=====")
packer = struct.Struct('i3si')
with open('dates.bin', 'wb') as f:
    for i in range(5):
        values = (2020 + i, b'jan', 10 + i)
        packed_data = packer.pack(*values)
        f.write(packed_data)
with open('dates.bin', 'rb') as f:
    f.seek(packer.size * 3)
    data = f.read(packer.size)

print(packer.unpack(data))

print("=====")
st = "hello"
print(st.encode())
d = struct.pack("8s" , st.encode())
print(d)
(e,) = struct.unpack("8s", d)
print(e.decode())
print(e.strip(b"\x00").decode().encode())
