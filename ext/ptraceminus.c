/*
 * python-ptraceplus - Ptrace bindings + extra stuff
 *
 * Copyright (c) 2013 Eric Le Bihan <eric.le.bihan.dev@free.fr>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <Python.h>
#include <sys/ptrace.h>

static PyObject *PtraceMinusError;

static inline PyObject*
ptrace_wrap1(int request, PyObject *self, PyObject *args)
{
        pid_t pid;
        long result;

        if (!PyArg_ParseTuple(args, "i", &pid))
                return NULL;

        result = ptrace(request, pid, 0, 0);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        Py_INCREF(Py_None);
        return Py_None;
}

static inline PyObject*
ptrace_wrap2(int request, PyObject *self, PyObject *args)
{
        pid_t pid;
        int data;
        long result;

        if (!PyArg_ParseTuple(args, "ii", &pid, &data))
                return NULL;

        result = ptrace(request, pid, 0, data);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        Py_INCREF(Py_None);
        return Py_None;
}

static inline PyObject*
ptrace_wrap4(int request, PyObject *self, PyObject *args)
{
        pid_t pid;
        long result, address, data;

        if (!PyArg_ParseTuple(args, "ill", &pid, &address, &data))
                return NULL;

        result = ptrace(request, pid, address, data);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        Py_INCREF(Py_None);
        return Py_None;
}

PyDoc_STRVAR(ptrace_traceme__doc__,
	     "traceme() -> None\n\n"
	     "Indicates that this process is to be traced by its\n"
	     "parent");

static PyObject*
ptrace_traceme(PyObject *self, PyObject *args)
{
        int result;

        if (!PyArg_ParseTuple(args, ""))
                return NULL;

        result = ptrace(PTRACE_TRACEME, 0, 0, 0);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        Py_INCREF(Py_None);
        return Py_None;
}

PyDoc_STRVAR(ptrace_attach__doc__,
	     "attach(pid) -> None\n\n"
	     "Attaches to the process specified in pid, making it a traced\n"
	     "'child' of the calling process.");

static PyObject*
ptrace_attach(PyObject *self, PyObject *args)
{
        return ptrace_wrap1(PTRACE_ATTACH, self, args);
}

PyDoc_STRVAR(ptrace_kill__doc__,
	     "kill(pid) -> None\n\n"
	     "Sends the child a SIGKILL to terminate it.");

static PyObject*
ptrace_kill(PyObject *self, PyObject *args)
{
        return ptrace_wrap1(PTRACE_KILL, self, args);
}

PyDoc_STRVAR(ptrace_cont__doc__,
	     "cont(pid, data=0) -> None\n\n"
	     "Restarts the stopped child process. If data is nonzero and not\n"
	     "SIGSTOP, it is interpreted as a signal to be delivered to the\n"
	     "child; otherwise, no signal is delivered.");

static PyObject*
ptrace_cont(PyObject *self, PyObject *args)
{
        return ptrace_wrap2(PTRACE_CONT, self, args);
}

PyDoc_STRVAR(ptrace_syscall__doc__,
	     "syscall(pid, data=0) -> None\n\n"
	     "Restarts the stopped child as for cont(), but arranges for the\n"
	     "child to be stopped at the next entry or exit from a system call.");

static PyObject*
ptrace_syscall(PyObject *self, PyObject *args)
{
        return ptrace_wrap2(PTRACE_SYSCALL, self, args);
}

PyDoc_STRVAR(ptrace_singlestep__doc__,
	     "singlstep(pid, data=0) -> None\n\n"
	     "Restarts the stopped child as for cont(), but arranges for the\n"
	     "child to be stopped after execution of a single step instruction.");

static PyObject*
ptrace_singlestep(PyObject *self, PyObject *args)
{
        return ptrace_wrap2(PTRACE_SINGLESTEP, self, args);
}

PyDoc_STRVAR(ptrace_detach__doc__,
	     "detach(pid) -> None\n\n"
	     "Restarts the stopped child as for cont(), but first detaches\n"
	     "from the process, undoing the reparenting effect of attach(),\n"
	     "and the effect of traceme().");

static PyObject*
ptrace_detach(PyObject *self, PyObject *args)
{
        return ptrace_wrap1(PTRACE_DETACH, self, args);
}

PyDoc_STRVAR(ptrace_poketext__doc__,
	     "poketext(addr, data) -> None\n\n"
	     "Copies the word data to location addr in the child's memory.");

static PyObject*
ptrace_poketext(PyObject *self, PyObject *args)
{
        return ptrace_wrap4(PTRACE_POKETEXT, self, args);
}

PyDoc_STRVAR(ptrace_pokedata__doc__,
	     "pokedata(addr, data) -> None\n\n"
	     "Copies the word data to location addr in the child's memory.");

static PyObject*
ptrace_pokedata(PyObject *self, PyObject *args)
{
        return ptrace_wrap4(PTRACE_POKEDATA, self, args);
}

PyDoc_STRVAR(ptrace_pokeuser__doc__,
	     "pokeuser(addr, data) -> None\n\n"
	     "Copies the word data to offset addr in the child's USER area");

static PyObject*
ptrace_pokeuser(PyObject *self, PyObject *args)
{
        return ptrace_wrap4(PTRACE_POKEUSER, self, args);
}

PyDoc_STRVAR(ptrace_setoptions__doc__,
	     "setoptions(pid, options) -> None\n\n"
	     "Sets ptrace options from data in the parent.");

static PyObject*
ptrace_setoptions(PyObject *self, PyObject *args)
{
        return ptrace_wrap2(PTRACE_SETOPTIONS, self, args);
}

PyDoc_STRVAR(ptrace_geteventmsg__doc__,
	     "geteventmsg(pid) -> int\n\n"
	     "Retrieves a message about the ptrace event that just happened.");

static PyObject*
ptrace_geteventmsg(PyObject *self, PyObject *args)
{
        pid_t pid;
        long data;
        long result;

        if (!PyArg_ParseTuple(args, "i", &pid))
                return NULL;

        result = ptrace(PTRACE_GETEVENTMSG, pid, 0, &data);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        return PyLong_FromUnsignedLong(data);
}

static inline PyObject*
ptrace_wrap2_return(int request, PyObject *self, PyObject *args)
{
        pid_t pid;
        long address;
        long result;

        if (!PyArg_ParseTuple(args, "il", &pid, &address))
                return NULL;

        result = ptrace(request, pid, address, 0);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        return PyLong_FromUnsignedLong(result & 0xffff);
}

PyDoc_STRVAR(ptrace_peektext__doc__,
	     "peektext(pid, addr) -> int\n\n"
	     "Reads a word at the location addr in the child's memory and\n"
	     "return it as an integer.");

static PyObject*
ptrace_peektext(PyObject *self, PyObject *args)
{
	return ptrace_wrap2_return(PTRACE_PEEKTEXT, self, args);
}

PyDoc_STRVAR(ptrace_peekdata__doc__,
	     "peekdata(pid, addr) -> int\n\n"
	     "Reads a word at the location addr in the child's memory and\n"
	     "return it as an integer.");

static PyObject*
ptrace_peekdata(PyObject *self, PyObject *args)
{
	return ptrace_wrap2_return(PTRACE_PEEKDATA, self, args);
}

PyDoc_STRVAR(ptrace_peekuser__doc__,
	     "peekuser(pid, addr) -> int\n\n"
	     "Reads a word at the location addr in the child's USER area and\n"
	     "return it as an integer.");

static PyObject*
ptrace_peekuser(PyObject *self, PyObject *args)
{
	return ptrace_wrap2_return(PTRACE_PEEKUSER, self, args);
}

static PyMethodDef
ptraceminus_methods[] = {
        { "traceme", ptrace_traceme, METH_VARARGS, ptrace_traceme__doc__ },
        { "attach", ptrace_attach, METH_VARARGS, ptrace_attach__doc__ },
        { "kill", ptrace_kill, METH_VARARGS, ptrace_kill__doc__ },
        { "cont", ptrace_cont, METH_VARARGS, ptrace_cont__doc__ },
        { "syscall", ptrace_syscall, METH_VARARGS, ptrace_syscall__doc__ },
        { "singlestep", ptrace_singlestep, METH_VARARGS, ptrace_singlestep__doc__ },
        { "detach", ptrace_detach, METH_VARARGS, ptrace_detach__doc__ },
        { "poketext", ptrace_poketext, METH_VARARGS, ptrace_poketext__doc__ },
        { "pokedata", ptrace_pokedata, METH_VARARGS, ptrace_pokedata__doc__ },
        { "pokeuser", ptrace_pokeuser, METH_VARARGS, ptrace_pokeuser__doc__ },
        { "setoptions", ptrace_setoptions, METH_VARARGS, ptrace_setoptions__doc__ },
        { "getventmsg", ptrace_geteventmsg, METH_VARARGS, ptrace_geteventmsg__doc__ },
        { "peektext", ptrace_peektext, METH_VARARGS, ptrace_peektext__doc__ },
        { "peekdata", ptrace_peekdata, METH_VARARGS, ptrace_peekdata__doc__ },
        { "peekuser", ptrace_peekuser, METH_VARARGS, ptrace_peekuser__doc__ },
        { NULL, NULL, 0, NULL },
};

static PyModuleDef
ptraceminus_mod = {
        PyModuleDef_HEAD_INIT,
        "ptraceminus",
        "Ptrace bindings",
        -1,
        ptraceminus_methods
};

PyMODINIT_FUNC
PyInit_ptraceminus(void)
{
        PyObject *m;

        m = PyModule_Create(&ptraceminus_mod);
        if (m == NULL)
                return NULL;

        PtraceMinusError = PyErr_NewExceptionWithDoc("ptraceminus.PtraceError",
						     "Error raised when Ptrace operation fails.",
						     NULL,
						     NULL);
        Py_INCREF(PtraceMinusError);
        PyModule_AddObject(m, "PtraceError", PtraceMinusError);

        PyModule_AddIntConstant(m, "O_TRACESYSGOOD", PTRACE_O_TRACESYSGOOD);
        PyModule_AddIntConstant(m, "O_TRACEFORK", PTRACE_O_TRACEFORK);
        PyModule_AddIntConstant(m, "O_TRACEVFORK", PTRACE_O_TRACEVFORK);
        PyModule_AddIntConstant(m, "O_TRACECLONE", PTRACE_O_TRACECLONE);
        PyModule_AddIntConstant(m, "O_TRACEEXEC", PTRACE_O_TRACEEXEC);
        PyModule_AddIntConstant(m, "O_TRACEEXIT", PTRACE_O_TRACEEXIT);
        PyModule_AddIntConstant(m, "O_TRACEVFORKDONE", PTRACE_O_TRACEVFORKDONE);
        PyModule_AddIntConstant(m, "EVENT_EXIT", PTRACE_EVENT_EXIT);
        PyModule_AddIntConstant(m, "EVENT_EXEC", PTRACE_EVENT_EXEC);
        PyModule_AddIntConstant(m, "EVENT_FORK", PTRACE_EVENT_FORK);
        PyModule_AddIntConstant(m, "EVENT_VFORK", PTRACE_EVENT_VFORK);

        return m;
}
