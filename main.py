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
from docopt import docopt
from process_utils import get_pid_by_port, kill_proc, display_net_connections


def main():
    # 2. 解析命令行
    arguments = docopt(__doc__, options_first=True)
    if arguments['--rm']:
        proc_pid = get_pid_by_port(int(arguments['<port>']))
        kill_proc(proc_pid)
    elif arguments['--version']:
        print("version")
    else:
        if (arguments['--tcp'] and arguments['--udp']) or (not arguments['--tcp'] and not arguments['--udp']):
            display_net_connections()
        elif arguments['--tcp']:
            display_net_connections(udp=False)
        elif arguments['--udp']:
            display_net_connections(tcp=False)
        else:
            pass


if __name__ == "__main__":
    main()