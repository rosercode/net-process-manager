Python 自动化运维- 基于 **psutil** 的 服务端口/网络进程 管理器



## 功能

- 列出所有正在监听端口的进程（即网络进程）
- 杀死指定端口的进程（网络进程）

## How To Use

### 列出进程

显示帮助信息

```bash
./net-process-manager --help
```

列出所有正在监听的端口

```bash
./net-process-manager
# or
./net-process-manager -l
# or
./net-process-manager --list
```

指定协议类型

```bash
# 列出所有的 TCP 
./net-process-manager -t
# 列出所有的 UDP
./net-process-manager -u
```

指定网络接口

```bash
./net-process-manager 127.0.0.1
# or
./net-process-manager eth0
```

### 杀死进程

通过指定端口

```bash
./net-process-manager -r <PORT>
```

通过进程的PID

```bash
./net-process-manager -r -p <PID>
./net-process-manager -r --pid <PID>
```

## 注意

这个命令并不提供额外的功能，比如 查看进程的更多信息，如果需要这方面的功能，推荐使用系统命令等方式

2022/11/23