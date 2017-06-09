import socket


host1 = "147.214.88.104"  #
host2 = "147.214.124.59"  #
host3 = "147.214.89.31"  #

host4 = "147.214.88.6"  #


def identify(host):
    port = 5025
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    f = s.makefile("rb")
    try:
        s.send(b"*IDN?\n")
        c = s.recv(1024)
        print(c.decode())
    finally:
        s.close()

for host in [host1, host2, host3, host4]:
    identify(host)
