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
various information. By default it prints all the system calls performed,
including the ones from the child processes spawned by the program traced.

The output of the program traced is suppressed, unless the option *--output*
is used to redirect the output of `ptraceplus(1)` to a file.

If the option *--stats* is set, some statistics on system calls will be
computed and printed (but not written to the output file).

OPTIONS
=======

-o FILE, --output=FILE      set output file
-s, --stats                 compute some statistics
-F, --full                  trace all events
-P NAME, --program=NAME     filter program by name
-S NAME, --syscall=NAME     filter syscall by name

SEE ALSO
========

- `strace(1)`

.. vim: ft=rst
