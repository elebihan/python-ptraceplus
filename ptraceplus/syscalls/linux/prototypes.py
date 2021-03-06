# -*- coding: utf-8 -*-
#
# python-ptraceplus - Ptrace bindings + extra stuff
#
# Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Syscall prototypes
"""

SYSCALL_PROTOS = {
    'setns': [('int', 'fd'), ('int', 'nstype')],
    'set_tid_address': [('int*', 'tidptr')],
    'fork': [],
    'vfork': [],
    'clone': [('unsigned long', 'clone_flags'), ('unsigned long', 'newsp'), ('int*', 'parent_tidpt')],
    'unshare': [('unsigned long', 'unshare_flags')],
    'utime': [('char*', 'filename'), ('struct utimbuf*', 'times')],
    'utimensat': [('int', 'dfd'), ('const char*', 'filename'), ('struct timespec*', 'utimes'), ('int', 'flag')],
    'futimesat': [('int', 'dfd'), ('const char*', 'filename'), ('struct timeval*', 'utime')],
    'utimes': [('char*', 'filename'), ('struct timeval*', 'utime')],
    'restart_syscall': [],
    'rt_sigprocmask': [('int', 'how'), ('sigset_t*', 'nset'), ('sigset_t*', 'oset'), ('size_t', 'sigsetsiz')],
    'rt_sigpending': [('sigset_t*', 'uset'), ('size_t', 'sigsetsize')],
    'rt_sigtimedwait': [('const sigset_t*', 'uthese'), ('siginfo_t*', 'uinfo'), ('const struct timespec*', 'ut')],
    'kill': [('pid_t', 'pid'), ('int', 'sig')],
    'tgkill': [('pid_t', 'tgid'), ('pid_t', 'pid'), ('int', 'sig')],
    'tkill': [('pid_t', 'pid'), ('int', 'sig')],
    'rt_sigqueueinfo': [('pid_t', 'pid'), ('int', 'sig'), ('siginfo_t*', 'uinf')],
    'rt_tgsigqueueinfo': [('pid_t', 'tgid'), ('pid_t', 'pid'), ('int', 'sig'), ('siginfo_t*', 'uinf')],
    'sigaltstack': [('const stack_t*', 'uss'), ('stack_t*', 'uoss')],
    'sigpending': [('old_sigset_t*', 'set')],
    'sigprocmask': [('int', 'how'), ('old_sigset_t*', 'nset'), ('old_sigset_t*', 'ose')],
    'rt_sigaction': [('int', 'sig'), ('const struct sigaction*', 'ac')],
    'sigaction': [('int', 'sig'), ('const struct old_sigaction*', 'ac')],
    'sgetmask': [],
    'ssetmask': [('int', 'newmask')],
    'signal': [('int', 'sig'), ('__sighandler_t', 'handler')],
    'pause': [],
    'rt_sigsuspend': [('sigset_t*', 'unewset'), ('size_t', 'sigsetsize')],
    'sigsuspend': [('old_sigset_t', 'mask')],
    'sigsuspend': [('int', 'unused1'), ('int', 'unused2'), ('old_sigset_t', 'mask')],
    'mprotect': [('unsigned long', 'start'), ('size_t', 'len'), ('unsigned long', 'pro')],
    'iopl': [('unsigned int', 'level')],
    'mknodat': [('int', 'dfd'), ('const char*', 'filename'), ('umode_t', 'mode'), ('unsigned', 'de')],
    'mknod': [('const char*', 'filename'), ('umode_t', 'mode'), ('unsigned', 'dev')],
    'mkdirat': [('int', 'dfd'), ('const char*', 'pathname'), ('umode_t', 'mode')],
    'mkdir': [('const char*', 'pathname'), ('umode_t', 'mode')],
    'rmdir': [('const char*', 'pathname')],
    'unlinkat': [('int', 'dfd'), ('const char*', 'pathname'), ('int', 'flag')],
    'unlink': [('const char*', 'pathname')],
    'symlinkat': [('const char*', 'oldname'), ('int', 'newdfd'), ('const char*', 'newnam')],
    'symlink': [('const char*', 'oldname'), ('const char*', 'newname')],
    'linkat': [('int', 'olddfd'), ('const char*', 'oldname'), ('int', 'newdfd'), ('const char*', 'newname'), ('int', 'flag')],
    'link': [('const char*', 'oldname'), ('const char*', 'newname')],
    'renameat': [('int', 'olddfd'), ('const char*', 'oldname'), ('int', 'newdfd'), ('const char*', 'newnam')],
    'rename': [('const char*', 'oldname'), ('const char*', 'newname')],
    'vm86old': [('struct vm86_struct*', 'v86')],
    'vm86': [('unsigned long', 'cmd'), ('unsigned long', 'arg')],
    'getitimer': [('int', 'which'), ('struct itimerval*', 'value')],
    'setitimer': [('int', 'which'), ('struct itimerval*', 'value'), ('struct itimerval*', 'ovalu')],
    'move_pages': [('pid_t', 'pid'), ('unsigned long', 'nr_pages'), ('const void**', 'page')],
    'eventfd2': [('unsigned int', 'count'), ('int', 'flags')],
    'eventfd': [('unsigned int', 'count')],
    'kcmp': [('pid_t', 'pid1'), ('pid_t', 'pid2'), ('int', 'type'), ('unsigned long', 'idx1'), ('unsigned long', 'idx')],
    'shmget': [('key_t', 'key'), ('size_t', 'size'), ('int', 'shmflg')],
    'shmctl': [('int', 'shmid'), ('int', 'cmd'), ('struct shmid_ds*', 'buf')],
    'shmat': [('int', 'shmid'), ('char*', 'shmaddr'), ('int', 'shmflg')],
    'shmdt': [('char*', 'shmaddr')],
    'mmap': [('unsigned long', 'addr'), ('unsigned long', 'len'), ('unsigned long', 'prot'), ('unsigned long', 'flag')],
    'ioprio_set': [('int', 'which'), ('int', 'who'), ('int', 'ioprio')],
    'ioprio_get': [('int', 'which'), ('int', 'who')],
    'readahead': [('int', 'fd'), ('loff_t', 'offset'), ('size_t', 'count')],
    'fanotify_init': [('unsigned int', 'flags'), ('unsigned int', 'event_f_flags')],
    'fanotify_mark': [('int', 'fanotify_fd'), ('unsigned int', 'flags'), ('__u64', 'mask'), ('int', 'df')],
    'ipc': [('unsigned int', 'call'), ('int', 'first'), ('unsigned long', 'second'), ('unsigned long', 'third'), ('void*', 'ptr'), ('long', 'fift')],
    'statfs': [('const char*', 'pathname'), ('struct statfs*', 'buf')],
    'statfs64': [('const char*', 'pathname'), ('size_t', 'sz'), ('struct statfs64*', 'buf')],
    'fstatfs': [('unsigned int', 'fd'), ('struct statfs*', 'buf')],
    'fstatfs64': [('unsigned int', 'fd'), ('size_t', 'sz'), ('struct statfs64*', 'buf')],
    'ustat': [('unsigned', 'dev'), ('struct ustat*', 'ubuf')],
    'capget': [('cap_user_header_t', 'header'), ('cap_user_data_t', 'dataptr')],
    'capset': [('cap_user_header_t', 'header'), ('const cap_user_data_t', 'data')],
    'remap_file_pages': [('unsigned long', 'start'), ('unsigned long', 'size'), ('unsigned long', 'prot'), ('unsigned long', 'pgoff'), ('unsigned long', 'flag')],
    'mq_open': [('const char*', 'u_name'), ('int', 'oflag'), ('umode_t', 'mode'), ('struct mq_attr*', 'u_att')],
    'mq_unlink': [('const char*', 'u_name')],
    'mq_timedsend': [('mqd_t', 'mqdes'), ('const char*', 'u_msg_ptr'), ('size_t', 'msg_len'), ('unsigned int', 'msg_pri')],
    'mq_timedreceive': [('mqd_t', 'mqdes'), ('char*', 'u_msg_ptr'), ('size_t', 'msg_len'), ('unsigned int*', 'u_msg_pri')],
    'mq_notify': [('mqd_t', 'mqdes'), ('const struct sigevent*', 'u_notificatio')],
    'mq_getsetattr': [('mqd_t', 'mqdes'), ('const struct mq_attr*', 'u_mqsta')],
    'lseek': [('unsigned int', 'fd'), ('off_t', 'offset'), ('unsigned int', 'whence')],
    'llseek': [('unsigned int', 'fd'), ('unsigned long', 'offset_high'), ('unsigned long', 'offset_low'), ('loff_t*', 'resul')],
    'read': [('unsigned int', 'fd'), ('char*', 'buf'), ('size_t', 'count')],
    'write': [('unsigned int', 'fd'), ('const char*', 'buf'), ('size_t', 'coun')],
    'pread64': [('unsigned int', 'fd'), ('char*', 'buf'), ('size_t', 'count'), ('loff_t', 'po')],
    'pwrite64': [('unsigned int', 'fd'), ('const char*', 'buf'), ('size_t', 'count'), ('loff_t', 'po')],
    'readv': [('unsigned long', 'fd'), ('const struct iovec*', 'vec'), ('unsigned long', 'vle')],
    'writev': [('unsigned long', 'fd'), ('const struct iovec*', 'vec'), ('unsigned long', 'vle')],
    'preadv': [('unsigned long', 'fd'), ('const struct iovec*', 'vec'), ('unsigned long', 'vlen'), ('unsigned long', 'pos_l'), ('unsigned long', 'pos_')],
    'pwritev': [('unsigned long', 'fd'), ('const struct iovec*', 'vec'), ('unsigned long', 'vlen'), ('unsigned long', 'pos_l'), ('unsigned long', 'pos_')],
    'sendfile': [('int', 'out_fd'), ('int', 'in_fd'), ('off_t*', 'offset'), ('size_t', 'count')],
    'sendfile64': [('int', 'out_fd'), ('int', 'in_fd'), ('loff_t*', 'offset'), ('size_t', 'count')],
    'fadvise64_64': [('int', 'fd'), ('loff_t', 'offset'), ('loff_t', 'len'), ('int', 'advice')],
    'fadvise64': [('int', 'fd'), ('loff_t', 'offset'), ('size_t', 'len'), ('int', 'advice')],
    'mremap': [('unsigned long', 'addr'), ('unsigned long', 'old_len'), ('unsigned long', 'new_len'), ('unsigned long', 'flag')],
    'set_thread_area': [('struct user_desc*', 'user_desc')],
    'get_thread_area': [('struct user_desc*', 'user_desc')],
    'stat': [('const char*', 'filename'), ('struct __old_kernel_stat*', 'statbu')],
    'lstat': [('const char*', 'filename'), ('struct __old_kernel_stat*', 'statbu')],
    'fstat': [('unsigned int', 'fd'), ('struct __old_kernel_stat*', 'statbuf')],
    'newstat': [('const char*', 'filename'), ('struct stat*', 'statbu')],
    'newlstat': [('const char*', 'filename'), ('struct stat*', 'statbu')],
    'newfstatat': [('int', 'dfd'), ('const char*', 'filename'), ('struct stat*', 'statbuf'), ('int', 'fla')],
    'newfstat': [('unsigned int', 'fd'), ('struct stat*', 'statbuf')],
    'readlinkat': [('int', 'dfd'), ('const char*', 'pathname'), ('char*', 'buf'), ('int', 'bufsi')],
    'readlink': [('const char*', 'path'), ('char*', 'buf'), ('int', 'bufsi')],
    'stat64': [('const char*', 'filename'), ('struct stat64*', 'statbu')],
    'lstat64': [('const char*', 'filename'), ('struct stat64*', 'statbu')],
    'fstat64': [('unsigned long', 'fd'), ('struct stat64*', 'statbuf')],
    'fstatat64': [('int', 'dfd'), ('const char*', 'filename'), ('struct stat64*', 'statbuf'), ('int', 'fla')],
    'msync': [('unsigned long', 'start'), ('size_t', 'len'), ('int', 'flags')],
    'socket': [('int', 'family'), ('int', 'type'), ('int', 'protocol')],
    'socketpair': [('int', 'family'), ('int', 'type'), ('int', 'protocol'), ('int*', 'usockve')],
    'bind': [('int', 'fd'), ('struct sockaddr*', 'umyaddr'), ('int', 'addrlen')],
    'listen': [('int', 'fd'), ('int', 'backlog')],
    'accept4': [('int', 'fd'), ('struct sockaddr*', 'upeer_sockaddr'), ('int*', 'upeer_addrlen'), ('int', 'flag')],
    'accept': [('int', 'fd'), ('struct sockaddr*', 'upeer_sockaddr'), ('int*', 'upeer_addrle')],
    'connect': [('int', 'fd'), ('struct sockaddr*', 'uservaddr'), ('int', 'addrle')],
    'getsockname': [('int', 'fd'), ('struct sockaddr*', 'usockaddr'), ('int*', 'usockaddr_le')],
    'getpeername': [('int', 'fd'), ('struct sockaddr*', 'usockaddr'), ('int*', 'usockaddr_le')],
    'sendto': [('int', 'fd'), ('void*', 'buff'), ('size_t', 'len'), ('unsigned int', 'flags'), ('struct sockaddr*', 'add')],
    'send': [('int', 'fd'), ('void*', 'buff'), ('size_t', 'len'), ('unsigned int', 'flag')],
    'recvfrom': [('int', 'fd'), ('void*', 'ubuf'), ('size_t', 'size'), ('unsigned int', 'flags'), ('struct sockaddr*', 'add')],
    'setsockopt': [('int', 'fd'), ('int', 'level'), ('int', 'optname'), ('char*', 'optval'), ('int', 'optle')],
    'getsockopt': [('int', 'fd'), ('int', 'level'), ('int', 'optname'), ('char*', 'optval'), ('int*', 'optle')],
    'shutdown': [('int', 'fd'), ('int', 'how')],
    'sendmsg': [('int', 'fd'), ('struct msghdr*', 'msg'), ('unsigned int', 'flags')],
    'sendmmsg': [('int', 'fd'), ('struct mmsghdr*', 'mmsg'), ('unsigned int', 'vlen'), ('unsigned int', 'flag')],
    'recvmsg': [('int', 'fd'), ('struct msghdr*', 'msg'), ('unsigned int', 'flag')],
    'recvmmsg': [('int', 'fd'), ('struct mmsghdr*', 'mmsg'), ('unsigned int', 'vlen'), ('unsigned int', 'flag')],
    'socketcall': [('int', 'call'), ('unsigned long*', 'args')],
    'nanosleep': [('struct timespec*', 'rqtp'), ('struct timespec*', 'rmt')],
    'brk': [('unsigned long', 'brk')],
    'mmap_pgoff': [('unsigned long', 'addr'), ('unsigned long', 'len'), ('unsigned long', 'prot'), ('unsigned long', 'flag')],
    'old_mmap': [('struct mmap_arg_struct*', 'arg')],
    'munmap': [('unsigned long', 'addr'), ('size_t', 'len')],
    'mremap': [('unsigned long', 'addr'), ('unsigned long', 'old_len'), ('unsigned long', 'new_len'), ('unsigned long', 'flag')],
    'ptrace': [('long', 'request'), ('long', 'pid'), ('unsigned long', 'addr'), ('unsigned long', 'dat')],
    'signalfd4': [('int', 'ufd'), ('sigset_t*', 'user_mask'), ('size_t', 'sizemask'), ('int', 'flag')],
    'signalfd': [('int', 'ufd'), ('sigset_t*', 'user_mask'), ('size_t', 'sizemas')],
    'dup3': [('unsigned int', 'oldfd'), ('unsigned int', 'newfd'), ('int', 'flags')],
    'dup2': [('unsigned int', 'oldfd'), ('unsigned int', 'newfd')],
    'dup': [('unsigned int', 'fildes')],
    'epoll_create1': [('int', 'flags')],
    'epoll_create': [('int', 'size')],
    'epoll_ctl': [('int', 'epfd'), ('int', 'op'), ('int', 'fd'), ('struct epoll_event*', 'even')],
    'epoll_wait': [('int', 'epfd'), ('struct epoll_event*', 'events'), ('int', 'maxevents'), ('int', 'timeou')],
    'epoll_pwait': [('int', 'epfd'), ('struct epoll_event*', 'events'), ('int', 'maxevents'), ('int', 'timeout'), ('const sigset_t*', 'sigmas')],
    'umount': [('char*', 'name'), ('int', 'flags')],
    'oldumount': [('char*', 'name')],
    'mount': [('char*', 'dev_name'), ('char*', 'dir_name'), ('char*', 'type'), ('unsigned long', 'flags'), ('void*', 'dat')],
    'pivot_root': [('const char*', 'new_root'), ('const char*', 'put_ol')],
    'acct': [('const char*', 'name')],
    'semget': [('key_t', 'key'), ('int', 'nsems'), ('int', 'semflg')],
    'semctl': [('int', 'semid'), ('int', 'semnum'), ('int', 'cmd'), ('unsigned long', 'arg')],
    'semtimedop': [('int', 'semid'), ('struct sembuf*', 'tsops'), ('unsigned', 'nsops'), ('const struct timespec*', 'timeou')],
    'semop': [('int', 'semid'), ('struct sembuf*', 'tsops'), ('unsigned', 'nsop')],
    'nice': [('int', 'increment')],
    'sched_setscheduler': [('pid_t', 'pid'), ('int', 'policy'), ('struct sched_param*', 'para')],
    'sched_setparam': [('pid_t', 'pid'), ('struct sched_param*', 'param')],
    'sched_getscheduler': [('pid_t', 'pid')],
    'sched_getparam': [('pid_t', 'pid'), ('struct sched_param*', 'param')],
    'sched_setaffinity': [('pid_t', 'pid'), ('unsigned int', 'len'), ('unsigned long*', 'user_mask_pt')],
    'sched_getaffinity': [('pid_t', 'pid'), ('unsigned int', 'len'), ('unsigned long*', 'user_mask_pt')],
    'sched_yield': [],
    'sched_get_priority_max': [('int', 'policy')],
    'sched_get_priority_min': [('int', 'policy')],
    'sched_rr_get_interval': [('pid_t', 'pid'), ('struct timespec*', 'interva')],
    'fcntl': [('unsigned int', 'fd'), ('unsigned int', 'cmd'), ('unsigned long', 'arg')],
    'fcntl64': [('unsigned int', 'fd'), ('unsigned int', 'cmd'), ('unsigned long', 'ar')],
    'pciconfig_read': [('unsigned long', 'bus'), ('unsigned long', 'dfn'), ('unsigned long', 'off'), ('unsigned long', 'len'), ('void*', 'bu')],
    'pciconfig_write': [('unsigned long', 'bus'), ('unsigned long', 'dfn'), ('unsigned long', 'off'), ('unsigned long', 'len'), ('void*', 'bu')],
    'mincore': [('unsigned long', 'start'), ('size_t', 'len'), ('unsigned char*', 've')],
    'sysctl': [('struct __sysctl_args*', 'args')],
    'brk': [('unsigned long', 'brk')],
    'mmap_pgoff': [('unsigned long', 'addr'), ('unsigned long', 'len'), ('unsigned long', 'prot'), ('unsigned long', 'flag')],
    'old_mmap': [('struct mmap_arg_struct*', 'arg')],
    'munmap': [('unsigned long', 'addr'), ('size_t', 'len')],
    'select': [('int', 'n'), ('fd_set*', 'inp'), ('fd_set*', 'outp'), ('fd_set*', 'exp'), ('struct timeval*', 'tv')],
    'pselect6': [('int', 'n'), ('fd_set*', 'inp'), ('fd_set*', 'outp'), ('fd_set*', 'exp'), ('struct timespec*', 'ts')],
    'old_select': [('struct sel_arg_struct*', 'arg')],
    'poll': [('struct pollfd*', 'ufds'), ('unsigned int', 'nfds'), ('int', 'timeout_msec')],
    'ppoll': [('struct pollfd*', 'ufds'), ('unsigned int', 'nfds'), ('struct timespec*', 'tsp'), ('const sigset_t*', 'sigmas')],
    'perf_event_open': [('struct perf_event_attr*', 'attr_upt')],
    'set_robust_list': [('struct robust_list_head*', 'head'), ('size_t', 'le')],
    'get_robust_list': [('int', 'pid'), ('struct robust_list_head**', 'head_pt')],
    'futex': [('u32*', 'uaddr'), ('int', 'op'), ('u32', 'val'), ('struct timespec*', 'utime'), ('u32*', 'uaddr')],
    'truncate': [('const char*', 'path'), ('long', 'length')],
    'ftruncate': [('unsigned int', 'fd'), ('unsigned long', 'length')],
    'truncate64': [('const char*', 'path'), ('loff_t', 'length')],
    'ftruncate64': [('unsigned int', 'fd'), ('loff_t', 'length')],
    'fallocate': [('int', 'fd'), ('int', 'mode'), ('loff_t', 'offset'), ('loff_t', 'len')],
    'faccessat': [('int', 'dfd'), ('const char*', 'filename'), ('int', 'mode')],
    'access': [('const char*', 'filename'), ('int', 'mode')],
    'chdir': [('const char*', 'filename')],
    'fchdir': [('unsigned int', 'fd')],
    'chroot': [('const char*', 'filename')],
    'fchmod': [('unsigned int', 'fd'), ('umode_t', 'mode')],
    'fchmodat': [('int', 'dfd'), ('const char*', 'filename'), ('umode_t', 'mode')],
    'chmod': [('const char*', 'filename'), ('umode_t', 'mode')],
    'fchownat': [('int', 'dfd'), ('const char*', 'filename'), ('uid_t', 'user'), ('gid_t', 'group'), ('int', 'fla')],
    'chown': [('const char*', 'filename'), ('uid_t', 'user'), ('gid_t', 'group')],
    'lchown': [('const char*', 'filename'), ('uid_t', 'user'), ('gid_t', 'group')],
    'fchown': [('unsigned int', 'fd'), ('uid_t', 'user'), ('gid_t', 'group')],
    'open': [('const char*', 'filename'), ('int', 'flags'), ('umode_t', 'mode')],
    'openat': [('int', 'dfd'), ('const char*', 'filename'), ('int', 'flags'), ('umode_t', 'mod')],
    'creat': [('const char*', 'pathname'), ('umode_t', 'mode')],
    'close': [('unsigned int', 'fd')],
    'vhangup': [],
    'mlock': [('unsigned long', 'start'), ('size_t', 'len')],
    'munlock': [('unsigned long', 'start'), ('size_t', 'len')],
    'mlockall': [('int', 'flags')],
    'munlockall': [],
    'vmsplice': [('int', 'fd'), ('const struct iovec*', 'iov'), ('unsigned long', 'nr_segs'), ('unsigned int', 'flag')],
    'splice': [('int', 'fd_in'), ('loff_t*', 'off_in'), ('int', 'fd_out'), ('loff_t*', 'off_ou')],
    'tee': [('int', 'fdin'), ('int', 'fdout'), ('size_t', 'len'), ('unsigned int', 'flags')],
    'set_thread_area': [('struct user_desc*', 'u_info')],
    'get_thread_area': [('struct user_desc*', 'u_info')],
    'swapoff': [('const char*', 'specialfile')],
    'swapon': [('const char*', 'specialfile'), ('int', 'swap_flags')],
    'process_vm_readv': [('pid_t', 'pid'), ('const struct iovec*', 'lvec'), ('unsigned long', 'liovcnt'), ('const struct iovec*', 'rve')],
    'process_vm_writev': [('pid_t', 'pid'), ('const struct iovec*', 'lve')],
    'bdflush': [('int', 'func'), ('long', 'data')],
    'timer_create': [('const clockid_t', 'which_clock'), ('struct sigevent*', 'timer_event_spe')],
    'timer_gettime': [('timer_t', 'timer_id'), ('struct itimerspec*', 'settin')],
    'timer_getoverrun': [('timer_t', 'timer_id')],
    'timer_settime': [('timer_t', 'timer_id'), ('int', 'flags'), ('const struct itimerspec*', 'new_settin')],
    'timer_delete': [('timer_t', 'timer_id')],
    'clock_settime': [('const clockid_t', 'which_clock'), ('const struct timespec*', 't')],
    'clock_gettime': [('const clockid_t', 'which_clock'), ('struct timespec*', 't')],
    'clock_adjtime': [('const clockid_t', 'which_clock'), ('struct timex*', 'ut')],
    'clock_getres': [('const clockid_t', 'which_clock'), ('struct timespec*', 't')],
    'clock_nanosleep': [('const clockid_t', 'which_clock'), ('int', 'flags'), ('const struct timespec*', 'rqt')],
    'reboot': [('int', 'magic1'), ('int', 'magic2'), ('unsigned int', 'cmd'), ('void*', 'ar')],
    'chown16': [('const char*', 'filename'), ('old_uid_t', 'user'), ('old_gid_t', 'group')],
    'lchown16': [('const char*', 'filename'), ('old_uid_t', 'user'), ('old_gid_t', 'group')],
    'fchown16': [('unsigned int', 'fd'), ('old_uid_t', 'user'), ('old_gid_t', 'group')],
    'setregid16': [('old_gid_t', 'rgid'), ('old_gid_t', 'egid')],
    'setgid16': [('old_gid_t', 'gid')],
    'setreuid16': [('old_uid_t', 'ruid'), ('old_uid_t', 'euid')],
    'setuid16': [('old_uid_t', 'uid')],
    'setresuid16': [('old_uid_t', 'ruid'), ('old_uid_t', 'euid'), ('old_uid_t', 'suid')],
    'getresuid16': [('old_uid_t*', 'ruidp'), ('old_uid_t*', 'euidp'), ('old_uid_t*', 'suidp')],
    'setresgid16': [('old_gid_t', 'rgid'), ('old_gid_t', 'egid'), ('old_gid_t', 'sgid')],
    'getresgid16': [('old_gid_t*', 'rgidp'), ('old_gid_t*', 'egidp'), ('old_gid_t*', 'sgidp')],
    'setfsuid16': [('old_uid_t', 'uid')],
    'setfsgid16': [('old_gid_t', 'gid')],
    'getgroups16': [('int', 'gidsetsize'), ('old_gid_t*', 'grouplist')],
    'setgroups16': [('int', 'gidsetsize'), ('old_gid_t*', 'grouplist')],
    'getuid16': [],
    'geteuid16': [],
    'getgid16': [],
    'getegid16': [],
    'add_key': [('const char*', '_type'), ('const char*', '_descriptio')],
    'request_key': [('const char*', '_type'), ('const char*', '_descriptio')],
    'keyctl': [('int', 'option'), ('unsigned long', 'arg2'), ('unsigned long', 'arg3'), ('unsigned long', 'arg4'), ('unsigned long', 'arg')],
    'getgroups': [('int', 'gidsetsize'), ('gid_t*', 'grouplist')],
    'setgroups': [('int', 'gidsetsize'), ('gid_t*', 'grouplist')],
    'delete_module': [('const char*', 'name_user'), ('unsigned int', 'flag')],
    'init_module': [('void*', 'umod'), ('unsigned long', 'len'), ('const char*', 'uarg')],
    'finit_module': [('int', 'fd'), ('const char*', 'uargs'), ('int', 'flags')],
    'syslog': [('int', 'type'), ('char*', 'buf'), ('int', 'len')],
    'time': [('time_t*', 'tloc')],
    'stime': [('time_t*', 'tptr')],
    'gettimeofday': [('struct timeval*', 'tv'), ('struct timezone*', 't')],
    'settimeofday': [('struct timeval*', 'tv'), ('struct timezone*', 't')],
    'adjtimex': [('struct timex*', 'txc_p')],
    'ioctl': [('unsigned int', 'fd'), ('unsigned int', 'cmd'), ('unsigned long', 'arg')],
    'setpriority': [('int', 'which'), ('int', 'who'), ('int', 'niceval')],
    'getpriority': [('int', 'which'), ('int', 'who')],
    'setregid': [('gid_t', 'rgid'), ('gid_t', 'egid')],
    'setgid': [('gid_t', 'gid')],
    'setreuid': [('uid_t', 'ruid'), ('uid_t', 'euid')],
    'setuid': [('uid_t', 'uid')],
    'setresuid': [('uid_t', 'ruid'), ('uid_t', 'euid'), ('uid_t', 'suid')],
    'getresuid': [('uid_t*', 'ruidp'), ('uid_t*', 'euidp'), ('uid_t*', 'suidp')],
    'setresgid': [('gid_t', 'rgid'), ('gid_t', 'egid'), ('gid_t', 'sgid')],
    'getresgid': [('gid_t*', 'rgidp'), ('gid_t*', 'egidp'), ('gid_t*', 'sgidp')],
    'setfsuid': [('uid_t', 'uid')],
    'setfsgid': [('gid_t', 'gid')],
    'getpid': [],
    'gettid': [],
    'getppid': [],
    'getuid': [],
    'geteuid': [],
    'getgid': [],
    'getegid': [],
    'times': [('struct tms*', 'tbuf')],
    'setpgid': [('pid_t', 'pid'), ('pid_t', 'pgid')],
    'getpgid': [('pid_t', 'pid')],
    'getpgrp': [],
    'getsid': [('pid_t', 'pid')],
    'setsid': [],
    'newuname': [('struct new_utsname*', 'name')],
    'uname': [('struct old_utsname*', 'name')],
    'olduname': [('struct oldold_utsname*', 'name')],
    'sethostname': [('char*', 'name'), ('int', 'len')],
    'gethostname': [('char*', 'name'), ('int', 'len')],
    'setdomainname': [('char*', 'name'), ('int', 'len')],
    'getrlimit': [('unsigned int', 'resource'), ('struct rlimit*', 'rlim')],
    'old_getrlimit': [('unsigned int', 'resource'), ('struct rlimit*', 'rli')],
    'prlimit64': [('pid_t', 'pid'), ('unsigned int', 'resource'), ('const struct rlimit64*', 'new_rli')],
    'setrlimit': [('unsigned int', 'resource'), ('struct rlimit*', 'rlim')],
    'getrusage': [('int', 'who'), ('struct rusage*', 'ru')],
    'umask': [('int', 'mask')],
    'prctl': [('int', 'option'), ('unsigned long', 'arg2'), ('unsigned long', 'arg3'), ('unsigned long', 'arg4'), ('unsigned long', 'arg')],
    'getcpu': [('unsigned*', 'cpup'), ('unsigned*', 'nodep'), ('struct getcpu_cache*', 'unuse')],
    'sysinfo': [('struct sysinfo*', 'info')],
    'mbind': [('unsigned long', 'start'), ('unsigned long', 'len'), ('unsigned long', 'mode'), ('unsigned long*', 'nmas')],
    'set_mempolicy': [('int', 'mode'), ('unsigned long*', 'nmask'), ('unsigned long', 'maxnod')],
    'migrate_pages': [('pid_t', 'pid'), ('unsigned long', 'maxnode'), ('const unsigned long*', 'old_node')],
    'get_mempolicy': [('int*', 'policy'), ('unsigned long*', 'nmask'), ('unsigned long', 'maxnod')],
    'getcwd': [('char*', 'buf'), ('unsigned long', 'size')],
    'exit': [('int', 'error_code')],
    'exit_group': [('int', 'error_code')],
    'waitid': [('int', 'which'), ('pid_t', 'upid'), ('struct siginfo*', 'infop'), ('int', 'options'), ('struct rusage*', 'r')],
    'wait4': [('pid_t', 'upid'), ('int*', 'stat_addr'), ('int', 'options'), ('struct rusage*', 'r')],
    'waitpid': [('pid_t', 'pid'), ('int*', 'stat_addr'), ('int', 'options')],
    'pipe2': [('int*', 'fildes'), ('int', 'flags')],
    'pipe': [('int*', 'fildes')],
    'personality': [('unsigned int', 'personality')],
    'madvise': [('unsigned long', 'start'), ('size_t', 'len_in'), ('int', 'behavior')],
    'inotify_init1': [('int', 'flags')],
    'inotify_init': [],
    'inotify_add_watch': [('int', 'fd'), ('const char*', 'pathname'), ('u32', 'mas')],
    'inotify_rm_watch': [('int', 'fd'), ('__s32', 'wd')],
    'kexec_load': [('unsigned long', 'entry'), ('unsigned long', 'nr_segments'), ('struct kexec_segment*', 'segments'), ('unsigned long', 'flag')],
    'old_readdir': [('unsigned int', 'fd'), ('struct old_linux_dirent*', 'dirent'), ('unsigned int', 'coun')],
    'getdents': [('unsigned int', 'fd'), ('struct linux_dirent*', 'dirent'), ('unsigned int', 'coun')],
    'getdents64': [('unsigned int', 'fd'), ('struct linux_dirent64*', 'dirent'), ('unsigned int', 'coun')],
    'sync': [],
    'syncfs': [('int', 'fd')],
    'fsync': [('unsigned int', 'fd')],
    'fdatasync': [('unsigned int', 'fd')],
    'sync_file_range': [('int', 'fd'), ('loff_t', 'offset'), ('loff_t', 'nbytes'), ('unsigned int', 'flag')],
    'sync_file_range2': [('int', 'fd'), ('unsigned int', 'flags'), ('loff_t', 'offset'), ('loff_t', 'nbyte')],
    'sysfs': [('int', 'option'), ('unsigned long', 'arg1'), ('unsigned long', 'arg2')],
    'timerfd_create': [('int', 'clockid'), ('int', 'flags')],
    'timerfd_settime': [('int', 'ufd'), ('int', 'flags'), ('const struct itimerspec*', 'utm')],
    'timerfd_gettime': [('int', 'ufd'), ('struct itimerspec*', 'otmr')],
    'flock': [('unsigned int', 'fd'), ('unsigned int', 'cmd')],
    'msgget': [('key_t', 'key'), ('int', 'msgflg')],
    'msgctl': [('int', 'msqid'), ('int', 'cmd'), ('struct msqid_ds*', 'buf')],
    'msgsnd': [('int', 'msqid'), ('struct msgbuf*', 'msgp'), ('size_t', 'msgsz'), ('int', 'msgfl')],
    'msgrcv': [('int', 'msqid'), ('struct msgbuf*', 'msgp'), ('size_t', 'msgsz'), ('long', 'msgtyp'), ('int', 'msgfl')],
    'alarm': [('unsigned int', 'seconds')],
    'uselib': [('const char*', 'library')],
    'execve': [('const char*', 'filename'), ('const char**', 'argv'), ('const char**', 'envp')],
    'io_setup': [('unsigned', 'nr_events'), ('aio_context_t*', 'ctxp')],
    'io_destroy': [('aio_context_t', 'ctx')],
    'io_submit': [('aio_context_t', 'ctx_id'), ('long', 'nr'), ('struct iocb**', 'iocbp')],
    'io_cancel': [('aio_context_t', 'ctx_id'), ('struct iocb*', 'iocb'), ('struct io_event*', 'resul')],
    'io_getevents': [('aio_context_t', 'ctx_id'), ('long', 'min_n')],
    'name_to_handle_at': [('int', 'dfd'), ('const char*', 'name'), ('struct file_handle*', 'handle'), ('int*', 'mnt_i')],
    'open_by_handle_at': [('int', 'mountdirfd'), ('struct file_handle*', 'handl')],
    'lookup_dcookie': [('u64', 'cookie64'), ('char*', 'buf'), ('size_t', 'len')],
    'quotactl': [('unsigned int', 'cmd'), ('const char*', 'special'), ('qid_t', 'id'), ('void*', 'add')],
    'setxattr': [('const char*', 'pathname'), ('const char*', 'name'), ('const void*', 'valu')],
    'lsetxattr': [('const char*', 'pathname'), ('const char*', 'name'), ('const void*', 'valu')],
    'fsetxattr': [('int', 'fd'), ('const char*', 'name'), ('const void*', 'value'), ('size_t', 'size'), ('int', 'flag')],
    'getxattr': [('const char*', 'pathname'), ('const char*', 'name'), ('void*', 'value'), ('size_t', 'siz')],
    'lgetxattr': [('const char*', 'pathname'), ('const char*', 'name'), ('void*', 'value'), ('size_t', 'siz')],
    'fgetxattr': [('int', 'fd'), ('const char*', 'name'), ('void*', 'value'), ('size_t', 'siz')],
    'listxattr': [('const char*', 'pathname'), ('char*', 'list'), ('size_t', 'siz')],
    'llistxattr': [('const char*', 'pathname'), ('char*', 'list'), ('size_t', 'siz')],
    'flistxattr': [('int', 'fd'), ('char*', 'list'), ('size_t', 'size')],
    'removexattr': [('const char*', 'pathname'), ('const char*', 'nam')],
    'lremovexattr': [('const char*', 'pathname'), ('const char*', 'nam')],
    'fremovexattr': [('int', 'fd'), ('const char*', 'name')],
}
