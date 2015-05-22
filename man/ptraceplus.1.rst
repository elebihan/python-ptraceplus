==========
ptraceplus
==========

---------------------------
Execute and trace a program
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

The system calls to trace can be selected using the *--syscall* option.
The programs to trace can be selected using the *--program* option.

If the option *--stats* is set, some statistics on system calls will be
computed and printed (but not written to the output file).

If the option *--execution* is set, `ptraceplus(1)` will only trace the
execution of child programs. It will report the PID of the child program, the
parent PID, as well as the command run and its return code. If the *--files*
option is added, the files read or written by the child program will also be
reported. The report is formatted using YAML.

To run properly, `ptraceplus(1)` needs the traced program to restrain from
running multiple jobs simultaneously (for example, `make(1)` should be invoked
with *-j1* option).

OPTIONS
=======

-a, --args                  get arguments when tracing execution
-f, --files                 trace file access during execution
-o FILE, --output=FILE      set output file
-s, --stats                 compute some statistics
-x, --execution             trace only execution
-F, --full                  trace all events
-P NAME, --program=NAME     filter program by name
-S NAME, --syscall=NAME     filter syscall by name

EXAMPLES
========

To trace the system calls performed by program `foobar`::

  $ ptraceplus foobar

To trace all the events::

  $ ptraceplus -F foobar

To trace only calls to 'open' and 'write'::

  $ ptraceplus -S open -S write foobar

To list all the files read or written during the compilation of a project::

  $ ptraceplus -xf -P gcc -P cc1 -P ld -P as -o files.yml make -j 1

SEE ALSO
========

- `strace(1)`

.. vim: ft=rst
