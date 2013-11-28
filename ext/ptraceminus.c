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
#include <structmember.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/user.h>

#ifdef _MSC_VER
#ifdef _M_X86
#define ARCH_X86
#endif
#endif

#ifdef __GNUC__
#if defined(__i386__) || defined(__i486__) || defined(__i586__) || defined(__i686__)
#define ARCH_X86
#endif
#if defined(__x86_64__)
#define ARCH_X86_64
#endif
#endif

/* TODO: support other architectures */
#ifndef ARCH_X86
#error "Only x86 is supported"
#endif

enum {
        CPU_TYPE_UNKNOWN = 0,
        CPU_TYPE_X86,
        CPU_TYPE_X86_64,
};

static char *x86_reg_names[] = {
        "ebx", "ecx", "edx", "esi", "edi", "ebp", "eax",
        "xds", "xes", "xfs", "xgs",
        "orig_eax", "eip", "xcs", "eflags", "esp", "xss",
};

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))

typedef struct RegisterStore {
        PyObject_HEAD
        PyObject *regs;
        int cpu_type;
} RegisterStore;

static int
RegisterStore_init(RegisterStore *self, PyObject *args, PyObject *kwds)
{
        RegisterStore *store = (RegisterStore*)self;
        int err;
        int i;

#if defined(ARCH_X86)
        self->cpu_type = CPU_TYPE_X86;
#else
        self->cpu_type = CPU_TYPE_UNKNOWN;
#endif

        for (i = 0; i < ARRAY_SIZE(x86_reg_names); i++) {
                 err = PyDict_SetItemString(store->regs,
                                            x86_reg_names[i],
                                            PyLong_FromLong(0));
                 if (err != 0)
                         goto fail;
        }

        return 0;

fail:
        Py_XDECREF(store->regs);
        return -1;
}

static void
RegisterStore_dealloc(RegisterStore *self)
{
        Py_XDECREF(self->regs);
        Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject*
RegisterStore_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
        RegisterStore *self;

        self = (RegisterStore*)type->tp_alloc(type, 0);
        if (self == NULL)
                return NULL;

        self->regs = PyDict_New();
        if (self->regs == NULL) {
                Py_DECREF(self);
                return NULL;
        }

        return (PyObject*)self;
}

static PyObject*
RegisterStore_get_cpu_type(RegisterStore *self, void *closure)
{
        PyObject *result = PyLong_FromLong(self->cpu_type);
        return result;
}

static PyObject*
RegisterStore_get_names(RegisterStore *self, void *closure)
{
        RegisterStore *store = (RegisterStore*)self;
        PyObject *result = NULL;

        result = PyDict_Keys(store->regs);
        Py_INCREF(result);

        return result;
}

static int
RegisterStore_len(PyObject *self)
{
        RegisterStore *store = (RegisterStore*)self;
        return PyDict_Size(store->regs);
}

static PyObject*
RegisterStore_getitem(PyObject *self, PyObject *key)
{
        RegisterStore *store = (RegisterStore*)self;
        PyObject *item = NULL;

        if (!PyUnicode_Check(key)) {
                PyErr_SetString(PyExc_TypeError, "Key must be a string");
                return NULL;
        }

        if (PyDict_Contains(store->regs, key) != 1) {
                PyErr_SetString(PyExc_KeyError, "Invalid register name");
                return NULL;
        }

        item = PyDict_GetItem(store->regs, key);
        Py_INCREF(item);

        return item;
}

static int
RegisterStore_setitem(PyObject *self, PyObject *key, PyObject *value)
{
        RegisterStore *store = (RegisterStore*)self;

        if (!PyUnicode_Check(key)) {
                PyErr_SetString(PyExc_TypeError, "Key must be a string");
                return 1;
        }

        if (!PyLong_Check(value)) {
                PyErr_SetString(PyExc_TypeError, "Value must be an integer");
                return 1;
        }

        if (PyDict_Contains(store->regs, key) != 1) {
                PyErr_SetString(PyExc_KeyError, "Invalid register name");
                return 1;
        }

        return PyDict_SetItem(store->regs, key, value);
}

static PyObject*
RegisterStore_str(PyObject *self)
{
        RegisterStore *store = (RegisterStore*)self;
        PyObject *obj = NULL;
        PyObject *bytes = NULL;
        PyObject *key = NULL, *value = NULL;
        Py_ssize_t pos = 0;
        Py_ssize_t length = 0;
        Py_ssize_t size = 0;
        char *str = NULL, *tmp = NULL;
        long regval = 0;

        while (PyDict_Next(store->regs, &pos, &key, &value)) {
                bytes = PyUnicode_AsASCIIString(key);
                length += PyBytes_Size(bytes) + 1 + 2 + sizeof(long) * 2 + 1;
                Py_DECREF(bytes);
        }

        str = (char*)calloc(length + 1, sizeof(char));
        if (str == NULL) {
                PyErr_SetString(PyExc_MemoryError,
                                "not enough memory for string");
                return NULL;
        }

        tmp = str;
        pos = 0;

        while (PyDict_Next(store->regs, &pos, &key, &value)) {
                bytes = PyUnicode_AsASCIIString(key);
                size = PyBytes_Size(bytes) + 1 + 2 + sizeof(long) * 2 + 1;
                regval = PyLong_AsLong(value);
                snprintf(tmp,
                         size + 1,
                         "%s=0x%08x ",
                         PyBytes_AsString(bytes),
                         (unsigned int)regval);
                Py_DECREF(bytes);
                tmp += size;
        }

        obj = PyUnicode_FromStringAndSize(str, length - 1);

        free(str);
        return obj;
}

static PyMemberDef
RegisterStore_members[] = {
        { "_regs", T_OBJECT, offsetof(RegisterStore, regs), 0,
          "Registers of the CPU" },
        { NULL },
};

static PyMethodDef
RegisterStore_methods[] = {
        { NULL },
};

static PyGetSetDef
RegisterStore_getseters[] = {
        { "cpu_type",
          (getter)RegisterStore_get_cpu_type,
          NULL,
          "CPU type",
          NULL
        },
        { "names",
          (getter)RegisterStore_get_names,
          NULL,
          "Names of the registers",
          NULL
        },
        { NULL },
};

static PyMappingMethods RegisterStore_as_mapping = {
        RegisterStore_len,
        RegisterStore_getitem,
        RegisterStore_setitem,
};

static PyTypeObject
RegisterStoreType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "ptraceminus.RegisterStore",                    /* tp_name */
        sizeof(RegisterStore),                          /* tp_basicsize */
        0,                                              /* tp_itemsize */
        (destructor)RegisterStore_dealloc,              /* tp_dealloc */
        0,                                              /* tp_print */
        0,                                              /* tp_getattr */
        0,                                              /* tp_setattr */
        0,                                              /* tp_compare */
        0,                                              /* tp_repr */
        0,                                              /* tp_as_number */
        0,                                              /* tp_as_sequence */
        &RegisterStore_as_mapping,                      /* tp_as_mapping */
        0,                                              /* tp_hash */
        0,                                              /* tp_call */
        RegisterStore_str,                              /* tp_str */
        0,                                              /* tp_getattro */
        0,                                              /* tp_setattro */
        0,                                              /* tp_as_buffer */
        Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,       /* tp_flags*/
        "CPU registers storage",                        /* tp_doc */
        0,                                              /* tp_traverse */
        0,                                              /* tp_clear */
        0,                                              /* tp_richcompare */
        0,                                              /* tp_weaklistoffset */
        0,                                              /* tp_iter */
        0,                                              /* tp_iternext */
        RegisterStore_methods,                          /* tp_methods */
        RegisterStore_members,                          /* tp_members */
        RegisterStore_getseters,                        /* tp_getset */
        0,                                              /* tp_base */
        0,                                              /* tp_dict */
        0,                                              /* tp_descr_get */
        0,                                              /* tp_descr_set */
        0,                                              /* tp_dictoffset */
        (initproc)RegisterStore_init,                   /* tp_init */
        0,                                              /* tp_alloc */
        RegisterStore_new,                              /* tp_new */
};

static PyObject *PtraceMinusError;

static inline PyObject*
ptrace_wrap1(int request, PyObject *self, PyObject *args)
{
        pid_t pid;
        long result;

        if (!PyArg_ParseTuple(args, "i", &pid))
                return NULL;

        result = ptrace(request, pid, NULL, NULL);

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

        result = ptrace(request, pid, NULL, data);

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

        result = ptrace(PTRACE_TRACEME, 0, NULL, NULL);

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

        result = ptrace(PTRACE_GETEVENTMSG, pid, NULL, &data);

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

        errno = 0;
        result = ptrace(request, pid, address, NULL);

        if (errno != 0)
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

PyDoc_STRVAR(ptrace_getregs__doc__,
	     "getregs(pid) -> RegisterStore\n\n"
	     "Reads the process general purpose registers and return it as\n"
	     "a RegisterStore object.");

static PyObject*
ptrace_getregs(PyObject *self, PyObject *args)
{
        pid_t pid = 0;
        long result = 0;
	RegisterStore *store = NULL;
        struct user_regs_struct regs = { 0, };

        if (!PyArg_ParseTuple(args, "i", &pid))
                return NULL;

        result = ptrace(PTRACE_GETREGS, pid, NULL, &regs);

        if (result == -1)
                return PyErr_SetFromErrno(PyExc_OSError);

        store = (RegisterStore*)PyObject_CallObject((PyObject*)&RegisterStoreType,
                                                    NULL);
        if (store == NULL)
                return NULL;

        /* TODO: support other architectures */
        PyDict_SetItemString(store->regs, "ebx", PyLong_FromLong(regs.ebx));
        PyDict_SetItemString(store->regs, "ecx", PyLong_FromLong(regs.ecx));
        PyDict_SetItemString(store->regs, "edx", PyLong_FromLong(regs.edx));
        PyDict_SetItemString(store->regs, "esi", PyLong_FromLong(regs.esi));
        PyDict_SetItemString(store->regs, "ebp", PyLong_FromLong(regs.ebp));
        PyDict_SetItemString(store->regs, "eax", PyLong_FromLong(regs.eax));
        PyDict_SetItemString(store->regs, "xds", PyLong_FromLong(regs.xds));
        PyDict_SetItemString(store->regs, "xes", PyLong_FromLong(regs.xes));
        PyDict_SetItemString(store->regs, "xfs", PyLong_FromLong(regs.xfs));
        PyDict_SetItemString(store->regs, "xgs", PyLong_FromLong(regs.xgs));
        PyDict_SetItemString(store->regs, "orig_eax", PyLong_FromLong(regs.orig_eax));
        PyDict_SetItemString(store->regs, "eip", PyLong_FromLong(regs.eip));
        PyDict_SetItemString(store->regs, "xcs", PyLong_FromLong(regs.xcs));
        PyDict_SetItemString(store->regs, "eflags", PyLong_FromLong(regs.eflags));
        PyDict_SetItemString(store->regs, "esp", PyLong_FromLong(regs.esp));
        PyDict_SetItemString(store->regs, "xss", PyLong_FromLong(regs.xss));

        return (PyObject*)store;
}

PyDoc_STRVAR(ptrace_getscnr__doc__,
	     "getscnr(pid) -> int\n\n"
	     "Reads the syscall number for a child process.");

static PyObject*
ptrace_getscnr(PyObject *self, PyObject *args)
{
        pid_t pid = 0;
        long addr = 0;
        long result = 0;

        if (!PyArg_ParseTuple(args, "i", &pid))
                return NULL;

#if defined(ARCH_X86)
        addr = 4 * ORIG_EAX;
#endif
        errno = 0;
        result = ptrace(PTRACE_PEEKUSER, pid, addr, NULL);

        if (errno != 0)
                return PyErr_SetFromErrno(PyExc_OSError);

        return PyLong_FromLong(result);
}

static int
_ptrace_getdata(pid_t pid, void *addr, void *buffer, size_t size)
{
        size_t rem = size % sizeof(long);
        size_t count = 0;
        long result = 0;
        char *tmp = buffer;
        int i;

        while (size) {
                errno = 0;
                result = ptrace(PTRACE_PEEKDATA, pid, addr, NULL);
                if (errno != 0)
                        return -1;
                count = (size == rem)? rem: sizeof(long);
                for (i = 0; i < count; i++) {
                        tmp[i] = ((result >> (i * 8)) & 0xff);
                }
                size -= count;
                tmp += count;
                addr = (void*)(((long)addr) + sizeof(long));
        }

        return 0;
}

static PyObject*
_ptrace_getstr(pid_t pid, void *addr)
{
        void *tmp = NULL;
        long result = 0;
        char *str = NULL;
        size_t size = 0;
        unsigned char stop = 0;
        PyObject *obj = NULL;
        int i;

        tmp = addr;

        while (!stop) {
                errno = 0;
                result = ptrace(PTRACE_PEEKDATA, pid, tmp, NULL);
                if (errno != 0)
                        return PyErr_SetFromErrno(PyExc_OSError);
                for (i = 0; i < sizeof(long); i++) {
                        if (((result >> (i * 8)) & 0xff) == '\0') {
                                stop = 1;
                                break;
                        } else {
                                size++;
                        }
                }
                tmp = (void*)(((long)tmp) + sizeof(long));
        }

        str = (char*)calloc(size + 1, sizeof(char));
        if (str == NULL) {
                PyErr_SetString(PyExc_MemoryError,
                                "not enough memory for string");
                return NULL;
        }

        if (_ptrace_getdata(pid, addr, str, size + 1) == 0) {
                obj = PyUnicode_FromStringAndSize(str, size);
        }

        free(str);
        return obj;
}

PyDoc_STRVAR(ptrace_getstr__doc__,
	     "getstr(pid, addr) -> str\n\n"
	     "Reads a character string stored at given address.");

static PyObject*
ptrace_getstr(PyObject *self, PyObject *args)
{
        pid_t pid = 0;
        long addr = 0;

        if (!PyArg_ParseTuple(args, "ik", &pid, &addr))
                return NULL;

        return _ptrace_getstr(pid, (void*)addr);
}

PyDoc_STRVAR(ptrace_getstrv__doc__,
	     "getstr(pid, addr) -> []\n\n"
	     "Reads an array of character strings stored at given\n"
             "address.");

static PyObject*
ptrace_getstrv(PyObject *self, PyObject *args)
{
        pid_t pid = 0;
        long addr = 0;
        long result = 0;
        void *tmp = NULL;
        PyObject *str = NULL;
        PyObject *list = NULL;
        int err = 0;

        if (!PyArg_ParseTuple(args, "ik", &pid, &addr))
                return NULL;

        list = PyList_New(0);
        if (list == NULL)
                return NULL;

        tmp = (void*)addr;

        while (1) {
                errno = 0;
                result = ptrace(PTRACE_PEEKDATA, pid, tmp, NULL);
                if (errno != 0) {
                        err = 1;
                        break;
                }

                if (!result)
                        break;

                str = _ptrace_getstr(pid, (void*)result);
                if (str == NULL) {
                        err = 2;
                        break;
                }

                if (PyList_Append(list, str) == -1) {
                        err = 3;
                        break;
                }

                tmp = (void*)(((long)tmp) + sizeof(long));
        }

        if (err != 0) {
                Py_DECREF(list);
                return (err == 1)? PyErr_SetFromErrno(PyExc_OSError): NULL;
        }

        return list;
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
        { "getregs", ptrace_getregs, METH_VARARGS, ptrace_getregs__doc__ },
        { "getscnr", ptrace_getscnr, METH_VARARGS, ptrace_getscnr__doc__ },
        { "getstr", ptrace_getstr, METH_VARARGS, ptrace_getstr__doc__ },
        { "getstrv", ptrace_getstrv, METH_VARARGS, ptrace_getstrv__doc__ },
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

        if (PyType_Ready(&RegisterStoreType) < 0)
                return NULL;

        Py_INCREF(&RegisterStoreType);
        PyModule_AddObject(m, "RegisterStore", (PyObject*)&RegisterStoreType);

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

        PyModule_AddIntConstant(m, "CPU_TYPE_UNKNOWN", CPU_TYPE_UNKNOWN);
        PyModule_AddIntConstant(m, "CPU_TYPE_X86", CPU_TYPE_X86);
        PyModule_AddIntConstant(m, "CPU_TYPE_X86_64", CPU_TYPE_X86_64);

        return m;
}
