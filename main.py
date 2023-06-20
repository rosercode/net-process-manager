# ppm
# 1. 定义接口描述
"""port process manager 网络进程管理器

Usage:
  ppm
  ppm [-r | --rm] <port>
  ppm [-u | --tcp] [ -u | --udp]
  ppm (-h | --help)
  ppm (-v | --version)

Options:
  -r --rm       end one process by port number. 根据端口结束一个网络进程.
  -t --tcp      show all network tcp connect. 展示所有的 tcp 网络连接.
  -u --udp      show all network tcp connect. 展示所有的 udp 网络连接.
  -v --version  show version message. 展示版本信息.
  -h --help     Show help. 展示帮助信息.

"""
import psutil
import socket
from prettytable import PrettyTable
from docopt import docopt


def get_pid_by_port(port: int):
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


def main():
    # 2. 解析命令行
    arguments = docopt(__doc__, options_first=True)
    if arguments['--rm']:
        proc_pid = get_pid_by_port(int(arguments['<port>']))
        kill_proc(proc_pid)
    elif arguments['--version']:
        print("version")
    else:
        table = PrettyTable(['pid', 'name', 'tcp/udp', 'listening ip', 'port'])
        lc = psutil.net_connections('inet')
        # 生成表格并打印
        for c in lc:
            (ip, port) = c.laddr
            proto_s = "tcp" if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN else (
                "udp" if c.type == socket.SOCK_DGRAM else "")
            pid_s = str(c.pid) if c.pid else '(unknown)'
            if pid_s != "(unknown)":
                try:
                    p = psutil.Process(int(pid_s))
                    if (arguments['--tcp'] and arguments['--udp']) or (
                            not arguments['--tcp'] and not arguments['--udp']):
                        table.add_row([pid_s, p.name(), proto_s, ip, port])
                    elif arguments['--tcp'] and proto_s == 'tcp':
                        table.add_row([pid_s, p.name(), proto_s, ip, port])
                    elif arguments['--udp'] and proto_s == 'udp':
                        table.add_row([pid_s, p.name(), proto_s, ip, port])
                    else:
                        pass
                except Exception:
                    continue
            else:
                table.add_row([pid_s, "", proto_s, ip, port])
        print(table)


if __name__ == "__main__":
    main()