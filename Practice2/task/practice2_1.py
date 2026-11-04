import sys
import struct
import socket

if len(sys.argv) == 1:
    print(socket.gethostname())
elif sys.argv[1] == "port":
    print(socket.getservbyport(int(sys.argv[2]), "tcp"))
elif sys.argv[1] == "domain":
    print(socket.gethostbyname(sys.argv[2]))

#py .\practice2_1.py          
#LAPTOP-HELEN
#py .\practice2_1.py port 22
#ssh
#py .\practice2_1.py domain www.google.com
#142.251.156.119
