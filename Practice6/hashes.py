import binascii
import hashlib

test_string = "You must cut down the mightiest tree in the forest with a herring"
test_string = test_string.encode("UTF-8")

#CRC 32
print(binascii.crc32(test_string))
print(hex(binascii.crc32(test_string)))

#MD 5
m = hashlib.md5()
m.update(test_string)
print(m.hexdigest())
m.update(test_string)
print(m.hexdigest())

m2 = hashlib.md5()
m2.update(test_string)
m2.update(test_string)
print(m2.hexdigest())

m3 = hashlib.sha1()
m3.update(test_string)
print(m3.hexdigest())

