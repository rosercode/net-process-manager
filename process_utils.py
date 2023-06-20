import psutil
from prettytable import PrettyTable
import socket


def get_pid_by_port(port: int) -> int:
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                    return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def kill_proc(pid: int):
    try:
        process = psutil.Process(pid)  # 根据进程ID获取进程对象
        process.terminate()  # 终止进程
        print(f"进程 {pid} 已成功终止。")
    except psutil.NoSuchProcess:
        print(f"找不到进程 {pid}。")
    except psutil.AccessDenied:
        print(f"没有足够的权限终止进程 {pid}。")


def display_net_connections(tcp=True, udp=True):
    table = PrettyTable(['pid', 'name', 'tcp/udp', 'listening ip', 'port'])
    lc = psutil.net_connections('inet')

    for c in lc:
        (ip, port) = c.laddr
        proto_s = "tcp" if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN else (
            "udp" if c.type == socket.SOCK_DGRAM else "")
        pid_s = str(c.pid) if c.pid else '(unknown)'

        if pid_s != "(unknown)":
            try:
                p = psutil.Process(int(pid_s))
                if (tcp and udp) or (not tcp and not udp):
                    table.add_row([pid_s, p.name(), proto_s, ip, port])
                elif tcp and proto_s == 'tcp':
                    table.add_row([pid_s, p.name(), proto_s, ip, port])
                elif udp and proto_s == 'udp':
                    table.add_row([pid_s, p.name(), proto_s, ip, port])
            except Exception:
                continue
        else:
            table.add_row([pid_s, "", proto_s, ip, port])

    print(table)
