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


def kill_proc(pid):
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
    table = PrettyTable(['pid', 'name', 'tcp/udp', 'listening ip', 'port'])
    lc = psutil.net_connections('inet')
    process_list = []
    for c in lc:
        (ip, port) = c.laddr
        proto_s = "tcp" if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN else (
            "udp" if c.type == socket.SOCK_DGRAM else "")
        pid_s = str(c.pid) if c.pid else '(unknown)'
        try:
            p = psutil.Process(int(pid_s))
        except Exception:
            continue
        if pid_s != "(unknown)":
            process_list.append([pid_s, p.name(), proto_s, ip, port])
        else:
            process_list.append([pid_s, "", proto_s, ip, port])

    if arguments['--rm']:
        process_exists = False
        for process in process_list:
            if process[4] == int(arguments['<port>']):
                kill_proc(int(process[0]))
                process_exists = True
                print("The process that specifying port is {}, pid is {} has ended.".format(arguments['<port>'], process[0]))
                break
        if not process_exists:
            print("The process don't exist")
    elif arguments['--version']:
        print("version")
    else:
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