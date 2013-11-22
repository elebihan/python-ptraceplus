==========
ptraceplus
==========

---------------------------
Execute and trace a process
---------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2013 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

ptraceplus [OPTIONS] <arg> [<arg>, ...]

DESCRIPTION
===========

`ptraceplus(1)` executes a program and traces its execution, collecting
various information. By default it prints the number of processes traced when
finished (including child processes spawned by the program traced).

OPTIONS
=======

-v, --verbose               verbose mode
-S NAME, --syscall=NAME     filter syscall by its name

SEE ALSO
========

- `strace(1)`

.. vim: ft=rst
