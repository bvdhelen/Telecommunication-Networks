import socket

print(socket.gethostname())
print(socket.gethostbyname("www.google.com"))

print("=====")
hostname, aliases, addresses = socket.gethostbyname_ex("www.google.com")
print(hostname)
print(aliases)
print(addresses)

print("=====")
hostname, aliases, addrs = socket.gethostbyaddr("157.181.161.79")
print(hostname)


print("=====")
print(socket.getservbyport(22, "tcp"))
for i in range(1, 101):
    try:
        print(f"{i} {socket.getservbyport(i, "tcp")}")
    except:
        pass