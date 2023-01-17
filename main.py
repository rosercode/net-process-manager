import psutil
import socket
from prettytable import PrettyTable

table = PrettyTable(['pid', 'name', 'tcp/udp','listening ip','port'])

rows = []
lc = psutil.net_connections('inet')
for c in lc:
    (ip, port) = c.laddr
    proto_s = "tcp" if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN else ("udp" if c.type == socket.SOCK_DGRAM else "")
    pid_s = str(c.pid) if c.pid else '(unknown)'
    if pid_s != "(unknown)":
        try:
            p = psutil.Process(int(pid_s))
            table.add_row([pid_s,p.name(), proto_s, ip, port])
        except Exception:
            pass
    else:
        table.add_row([pid_s,"", proto_s, ip, port])
print(table)