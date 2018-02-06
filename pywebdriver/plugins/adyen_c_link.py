# pylint: skip-file
'''Wrapper for poslibc.h

Generated with:
../../ctypesgen/ctypesgen.py -ladyen_pos lib_include/poslibc.h lib_include/additional_data_obj.h lib_include/adyen_enum.h lib_include/balance_inquiry_extern.h lib_include/cancel_or_refund_extern.h lib_include/card_operation_request.h lib_include/create_special_tender_extern.h lib_include/create_tender_extern.h lib_include/library_extern.h lib_include/load_request_extern.h lib_include/obj_manager.h lib_include/ped_device_info.h lib_include/poslibc.h lib_include/receipt_data_obj.h lib_include/refund_extern.h lib_include/register_app_extern.h lib_include/register_device_extern.h lib_include/show_screen_extern.h lib_include/status_tender_response.h lib_include/tender_options_obj.h lib_include/tx_store_query_extern.h lib_include/update_tender_extern.h -o adyen_pos.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import platform
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        unix_lib_dirs_list = ['/lib', '/usr/lib', '/lib64', '/usr/lib64']
        if sys.platform.startswith('linux'):
            # Try and support multiarch work in Ubuntu
            # https://wiki.ubuntu.com/MultiarchSpec
            bitage = platform.architecture()[0]
            if bitage.startswith('32'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/i386-linux-gnu', '/usr/lib/i386-linux-gnu']
            elif bitage.startswith('64'):
                # Assume Intel/AMD x86 compat
                unix_lib_dirs_list += ['/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']
            else:
                # guess...
                unix_lib_dirs_list += glob.glob('/lib/*linux-gnu')
        directories.extend(unix_lib_dirs_list)

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["adyen_pos"] = load_library("adyen_pos")

# 1 libraries
# End libraries

# No modules

enum_anon_1 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 42

ADYboolFalse = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 42

ADYboolTrue = (ADYboolFalse + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 42

ADYbool = enum_anon_1 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 42

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 45
if hasattr(_libs['adyen_pos'], 'count_total_enum'):
    count_total_enum = _libs['adyen_pos'].count_total_enum
    count_total_enum.argtypes = [CFUNCTYPE(UNCHECKED(String), c_int)]
    count_total_enum.restype = c_int

ADYLibraryResult = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

enum_anon_2 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultOk = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultXmlToJsonConversionFailed = (ADYLibraryResultOk + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultJsonConstructionFailed = (ADYLibraryResultXmlToJsonConversionFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultJsonParsingFailed = (ADYLibraryResultJsonConstructionFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultXmlParsingFailed = (ADYLibraryResultJsonParsingFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoJaasToken = (ADYLibraryResultXmlParsingFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRcptNoData = (ADYLibraryResultNoJaasToken + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultResultUnknown = (ADYLibraryResultRcptNoData + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTooSmall = (ADYLibraryResultResultUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTooLarge = (ADYLibraryResultTooSmall + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInvalid = (ADYLibraryResultTooLarge + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultUpgrade = (ADYLibraryResultInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailCalloc = (ADYLibraryResultUpgrade + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalUndefinedFail = (ADYLibraryResultInternalFailCalloc + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalInstanceFail = (ADYLibraryResultInternalUndefinedFail + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalInvalidRefObj = (ADYLibraryResultInternalInstanceFail + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalMissingArgument = (ADYLibraryResultInternalInvalidRefObj + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailInit = (ADYLibraryResultInternalMissingArgument + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailGeneric = (ADYLibraryResultInternalFailInit + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailException = (ADYLibraryResultInternalFailGeneric + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailFatal = (ADYLibraryResultInternalFailException + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailPEDNotRegistered = (ADYLibraryResultInternalFailFatal + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailMUX = (ADYLibraryResultInternalFailPEDNotRegistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailJSON = (ADYLibraryResultInternalFailMUX + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailNotInitialized = (ADYLibraryResultInternalFailJSON + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalNoLibraryStruct = (ADYLibraryResultInternalFailNotInitialized + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalNoLibraryThread = (ADYLibraryResultInternalNoLibraryStruct + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalNoPipeIn = (ADYLibraryResultInternalNoLibraryThread + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalNoPipeOut = (ADYLibraryResultInternalNoPipeIn + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalFailUpdateTender = (ADYLibraryResultInternalNoPipeOut + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInternalCurlError = (ADYLibraryResultInternalFailUpdateTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultHttpErrorGeneral = (ADYLibraryResultInternalCurlError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoNetworkOrNoService = (ADYLibraryResultHttpErrorGeneral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNotAuthorised = (ADYLibraryResultNoNetworkOrNoService + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultHttpError500 = (ADYLibraryResultNotAuthorised + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultHttpError503NoService = (ADYLibraryResultHttpError500 + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTimeout = (ADYLibraryResultHttpError503NoService + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoService = (ADYLibraryResultTimeout + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultDnsLookupError = (ADYLibraryResultNoService + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoRoute = (ADYLibraryResultDnsLookupError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultFailedToConnect = (ADYLibraryResultNoRoute + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConnectionClosed = (ADYLibraryResultFailedToConnect + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultSslError = (ADYLibraryResultConnectionClosed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultUnspecifiedHttpError = (ADYLibraryResultSslError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInitializationRequestNull = (ADYLibraryResultUnspecifiedHttpError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInitializationNoCallback = (ADYLibraryResultInitializationRequestNull + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInitializationEnvironmentInvalid = (ADYLibraryResultInitializationNoCallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInitializationNoExceptionHandler = (ADYLibraryResultInitializationEnvironmentInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTerminalIDInvalid = (ADYLibraryResultInitializationNoExceptionHandler + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoPEDFound = (ADYLibraryResultTerminalIDInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTenderReferenceInvalid = (ADYLibraryResultNoPEDFound + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultReferenceMissing = (ADYLibraryResultTenderReferenceInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallback = (ADYLibraryResultReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterAppRequestNull = (ADYLibraryResultNoCallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterAppNoCallback = (ADYLibraryResultRegisterAppRequestNull + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultMerchantAccountMissing = (ADYLibraryResultRegisterAppNoCallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultUserIDMissing = (ADYLibraryResultMerchantAccountMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPasswordMissing = (ADYLibraryResultUserIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultAppIDMissing = (ADYLibraryResultPasswordMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterAppPSPNoResponse = (ADYLibraryResultAppIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterAppFailed = (ADYLibraryResultRegisterAppPSPNoResponse + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultIdentifyPEDFailed = (ADYLibraryResultRegisterAppFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceRequestNull = (ADYLibraryResultIdentifyPEDFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceNoCallback = (ADYLibraryResultRegisterDeviceRequestNull + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultDeviceAddressMissing = (ADYLibraryResultRegisterDeviceNoCallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultDeviceAddressEmpty = (ADYLibraryResultDeviceAddressMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForDeviceState = (ADYLibraryResultDeviceAddressEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForAdditionalData = (ADYLibraryResultNoCallbackForDeviceState + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForPrintReceipt = (ADYLibraryResultNoCallbackForAdditionalData + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForCheckSignature = (ADYLibraryResultNoCallbackForPrintReceipt + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForReferral = (ADYLibraryResultNoCallbackForCheckSignature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForBalanceAcquired = (ADYLibraryResultNoCallbackForReferral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultNoCallbackForFinal = (ADYLibraryResultNoCallbackForBalanceAcquired + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfiguredNameMissing = (ADYLibraryResultNoCallbackForFinal + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfiguredNameEmpty = (ADYLibraryResultConfiguredNameMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultInvalidNumberOfDeviceOptions = (ADYLibraryResultConfiguredNameEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPSPRegisterDeviceError = (ADYLibraryResultInvalidNumberOfDeviceOptions + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPSPSyncNoRequest = (ADYLibraryResultPSPRegisterDeviceError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPSPSyncNoConfig = (ADYLibraryResultPSPSyncNoRequest + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPSPSyncPSPError = (ADYLibraryResultPSPSyncNoConfig + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPSPSyncNoResponse = (ADYLibraryResultPSPSyncPSPError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPEDSyncError = (ADYLibraryResultPSPSyncNoResponse + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPEDSyncNoResponse = (ADYLibraryResultPEDSyncError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceFailed = (ADYLibraryResultPEDSyncNoResponse + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceTimeout = (ADYLibraryResultRegisterDeviceFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceSoapVersionNotSupported = (ADYLibraryResultRegisterDeviceTimeout + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRegisterDeviceExists = (ADYLibraryResultRegisterDeviceSoapVersionNotSupported + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCreateTenderRequestNull = (ADYLibraryResultRegisterDeviceExists + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTerminalIDMissing = (ADYLibraryResultCreateTenderRequestNull + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultTransactionTypeInvalid = (ADYLibraryResultTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultAmountCurrencyInvalid = (ADYLibraryResultTransactionTypeInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultAmountValueInvalid = (ADYLibraryResultAmountCurrencyInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultGratuityAmountCurrencyInvalid = (ADYLibraryResultAmountValueInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultGratuityAmountValueInvalid = (ADYLibraryResultGratuityAmountCurrencyInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultShopperEmailInvalid = (ADYLibraryResultGratuityAmountValueInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRecurringContractNameInvalid = (ADYLibraryResultShopperEmailInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultRecurringDetailNameInvalid = (ADYLibraryResultRecurringContractNameInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCreateTenderFailed = (ADYLibraryResultRecurringDetailNameInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelTenderTerminalIDInvalid = (ADYLibraryResultCreateTenderFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelTenderNoPEDFound = (ADYLibraryResultCancelTenderTerminalIDInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelTenderReferenceInvalid = (ADYLibraryResultCancelTenderNoPEDFound + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmAdditionalDataTerminalIDMissing = (ADYLibraryResultCancelTenderReferenceInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmAdditionalDataTerminalIDEmpty = (ADYLibraryResultConfirmAdditionalDataTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmAdditionalDataTerminalIDUnknown = (ADYLibraryResultConfirmAdditionalDataTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmAdditionalDataTenderReferenceMissing = (ADYLibraryResultConfirmAdditionalDataTerminalIDUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmAdditionalDataTenderReferenceEmpty = (ADYLibraryResultConfirmAdditionalDataTenderReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmPrintReceiptTerminalIDMissing = (ADYLibraryResultConfirmAdditionalDataTenderReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmPrintReceiptTerminalIDEmpty = (ADYLibraryResultConfirmPrintReceiptTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmPrintReceiptTerminalIDUnknown = (ADYLibraryResultConfirmPrintReceiptTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmPrintReceiptTenderReferenceMissing = (ADYLibraryResultConfirmPrintReceiptTerminalIDUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmPrintReceiptTenderReferenceEmpty = (ADYLibraryResultConfirmPrintReceiptTenderReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmReferralTerminalIDMissing = (ADYLibraryResultConfirmPrintReceiptTenderReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmReferralTerminalIDEmpty = (ADYLibraryResultConfirmReferralTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmReferralTerminalIDUnknown = (ADYLibraryResultConfirmReferralTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmReferralTenderReferenceMissing = (ADYLibraryResultConfirmReferralTerminalIDUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmReferralTenderReferenceEmpty = (ADYLibraryResultConfirmReferralTenderReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmSignatureTerminalIDMissing = (ADYLibraryResultConfirmReferralTenderReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmSignatureTerminalIDEmpty = (ADYLibraryResultConfirmSignatureTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmSignatureTerminalIDUnknown = (ADYLibraryResultConfirmSignatureTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmSignatureTenderReferenceMissing = (ADYLibraryResultConfirmSignatureTerminalIDUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultConfirmSignatureTenderReferenceEmpty = (ADYLibraryResultConfirmSignatureTenderReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultQueryPedStateTerminalIDMissing = (ADYLibraryResultConfirmSignatureTenderReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultQueryPedStateTerminalIDEmpty = (ADYLibraryResultQueryPedStateTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultQueryPedStateTerminalIDUnknown = (ADYLibraryResultQueryPedStateTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultQueryPedStateInvalidArguments = (ADYLibraryResultQueryPedStateTerminalIDUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultQueryPedStateInvalidState = (ADYLibraryResultQueryPedStateInvalidArguments + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundMerchantAccountMissing = (ADYLibraryResultQueryPedStateInvalidState + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundMerchantAccountEmpty = (ADYLibraryResultCancelorRefundMerchantAccountMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundOrgReferenceMissing = (ADYLibraryResultCancelorRefundMerchantAccountEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundOrgReferenceEmpty = (ADYLibraryResultCancelorRefundOrgReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundReferenceMissing = (ADYLibraryResultCancelorRefundOrgReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundReferenceEmpty = (ADYLibraryResultCancelorRefundReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundCallBackMissing = (ADYLibraryResultCancelorRefundReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundFailed = (ADYLibraryResultCancelorRefundCallBackMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSTenderReferenceMissing = (ADYLibraryResultCancelorRefundFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSTenderReferenceEmpty = (ADYLibraryResultCancelorRefundPOSTenderReferenceMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSTranscationTypeMissing = (ADYLibraryResultCancelorRefundPOSTenderReferenceEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSTranscationTypeEmpty = (ADYLibraryResultCancelorRefundPOSTranscationTypeMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSUniqueTerminalIDMissing = (ADYLibraryResultCancelorRefundPOSTranscationTypeEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultCancelorRefundPOSUniqueTerminalIDEmpty = (ADYLibraryResultCancelorRefundPOSUniqueTerminalIDMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultPaymentMethodTypeInvalid = (ADYLibraryResultCancelorRefundPOSUniqueTerminalIDEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultUnknown = (ADYLibraryResultPaymentMethodTypeInvalid + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

ADYLibraryResultLast = (ADYLibraryResultUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 55

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 66
if hasattr(_libs['adyen_pos'], 'get_adyen_library_result_text'):
    get_adyen_library_result_text = _libs['adyen_pos'].get_adyen_library_result_text
    get_adyen_library_result_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_adyen_library_result_text.restype = ReturnString
    else:
        get_adyen_library_result_text.restype = String
        get_adyen_library_result_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 69
if hasattr(_libs['adyen_pos'], 'get_adyen_library_result_enum'):
    get_adyen_library_result_enum = _libs['adyen_pos'].get_adyen_library_result_enum
    get_adyen_library_result_enum.argtypes = [String]
    get_adyen_library_result_enum.restype = ADYLibraryResult

ADYPEDResult = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

enum_anon_3 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultOk = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDDeprecated1 = (ADYPEDResultOk + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultFail = (ADYPEDDeprecated1 + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultSerialServer = (ADYPEDResultFail + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultSerialClient = (ADYPEDResultSerialServer + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultNotAllowed = (ADYPEDResultSerialClient + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultNoAmountSpecified = (ADYPEDResultNotAllowed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultUnableToDetermineVariant = (ADYPEDResultNoAmountSpecified + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidMerchantAccount = (ADYPEDResultUnableToDetermineVariant + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultRequestMissing = (ADYPEDResultInvalidMerchantAccount + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInternalError = (ADYPEDResultRequestMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultUnableToProcess = (ADYPEDResultInternalError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPaymentDetailsNotSupported = (ADYPEDResultUnableToProcess + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultSoapServer = (ADYPEDResultPaymentDetailsNotSupported + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInternalPSP = (ADYPEDResultSoapServer + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidApp = (ADYPEDResultInternalPSP + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidUser = (ADYPEDResultInvalidApp + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidDevice = (ADYPEDResultInvalidUser + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidMerchant = (ADYPEDResultInvalidDevice + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallIdentifyPaymentDeviceError = (ADYPEDResultInvalidMerchant + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallRegisterAppError = (ADYPEDResultCallIdentifyPaymentDeviceError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallRegisterDeviceError = (ADYPEDResultCallRegisterAppError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallSyncActionError = (ADYPEDResultCallRegisterDeviceError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallSynchroniseError = (ADYPEDResultCallSyncActionError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallCreateTenderError = (ADYPEDResultCallSynchroniseError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallStatusTenderError = (ADYPEDResultCallCreateTenderError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallupdatetenderError = (ADYPEDResultCallStatusTenderError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallDiagnoseSyncError = (ADYPEDResultCallupdatetenderError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCallLogSyncError = (ADYPEDResultCallDiagnoseSyncError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDDeprecated2 = (ADYPEDResultCallLogSyncError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTransactionDeclined = (ADYPEDDeprecated2 + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTransactionCancelled = (ADYPEDResultTransactionDeclined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTransactionError = (ADYPEDResultTransactionCancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTransactionReferral = (ADYPEDResultTransactionError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTerminalNotReady = (ADYPEDResultTransactionReferral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultAmountTooLow = (ADYPEDResultTerminalNotReady + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidTransactionType = (ADYPEDResultAmountTooLow + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCashbackNotSupported = (ADYPEDResultInvalidTransactionType + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultNoPrinterPresent = (ADYPEDResultCashbackNotSupported + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidCurrencyCode = (ADYPEDResultNoPrinterPresent + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCurrencyNotSupported = (ADYPEDResultInvalidCurrencyCode + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultAskGratuityOnlyWithGoodsServices = (ADYPEDResultCurrencyNotSupported + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMKENotAllowed = (ADYPEDResultAskGratuityOnlyWithGoodsServices + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultIncompatibleCurrencies = (ADYPEDResultMKENotAllowed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultGratuityTooLow = (ADYPEDResultIncompatibleCurrencies + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultGratuityTooHigh = (ADYPEDResultGratuityTooLow + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidDateSupplied = (ADYPEDResultGratuityTooHigh + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultDateAdjustementNotAllowed = (ADYPEDResultInvalidDateSupplied + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultUnfinishedTender = (ADYPEDResultDateAdjustementNotAllowed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultAmountTooHigh = (ADYPEDResultUnfinishedTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultRefundNotAllowed = (ADYPEDResultAmountTooHigh + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultDeviceNotRegistered = (ADYPEDResultRefundNotAllowed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCredentialsMissing = (ADYPEDResultDeviceNotRegistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCardRemovedDuringAppSelection = (ADYPEDResultCredentialsMissing + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultUpdateAmountFailed = (ADYPEDResultCardRemovedDuringAppSelection + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultResetCurrentTender = (ADYPEDResultUpdateAmountFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPrintReceiptTimeOut = (ADYPEDResultResetCurrentTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultAdjustAmountTimeOut = (ADYPEDResultPrintReceiptTimeOut + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultEMVDataAuthenticationFailed = (ADYPEDResultAdjustAmountTimeOut + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultEMVGenerateFirstAcFailed = (ADYPEDResultEMVDataAuthenticationFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultEMVReadApplicationFailed = (ADYPEDResultEMVGenerateFirstAcFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultEMVVerifyCardholderFailed = (ADYPEDResultEMVReadApplicationFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledAppSelection = (ADYPEDResultEMVVerifyCardholderFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledDuringPINEntry = (ADYPEDResultShopperCancelledAppSelection + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultFailedToPrintReceipt = (ADYPEDResultShopperCancelledDuringPINEntry + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantCancelledTransaction = (ADYPEDResultFailedToPrintReceipt + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultLibraryCancelledTransaction = (ADYPEDResultMerchantCancelledTransaction + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantDeclinedSignature = (ADYPEDResultLibraryCancelledTransaction + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPEDDeviceTimeOutCardEntry = (ADYPEDResultMerchantDeclinedSignature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCardRemoved = (ADYPEDResultPEDDeviceTimeOutCardEntry + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledTransaction = (ADYPEDResultCardRemoved + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperDeclinedSignature = (ADYPEDResultShopperCancelledTransaction + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledDuringDCCSelection = (ADYPEDResultShopperDeclinedSignature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledDuringMKE = (ADYPEDResultShopperCancelledDuringDCCSelection + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperDidNotEnterCard = (ADYPEDResultShopperCancelledDuringMKE + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultEMVError = (ADYPEDResultShopperDidNotEnterCard + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultSapiError = (ADYPEDResultEMVError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultFailedToRetrieveAdditionalData = (ADYPEDResultSapiError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCardOnReferralList = (ADYPEDResultFailedToRetrieveAdditionalData + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultBlockCard = (ADYPEDResultCardOnReferralList + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCardExpired = (ADYPEDResultBlockCard + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidAmount = (ADYPEDResultCardExpired + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidCard = (ADYPEDResultInvalidAmount + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultIssuerUnavailable = (ADYPEDResultInvalidCard + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultNotSupported = (ADYPEDResultIssuerUnavailable + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultNotEnoughBalance = (ADYPEDResultNotSupported + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPending = (ADYPEDResultNotEnoughBalance + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultAcquirerFraud = (ADYPEDResultPending + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTerminalInUse = (ADYPEDResultAcquirerFraud + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultReceiptNotPrinted = (ADYPEDResultTerminalInUse + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTerminalUnavailable = (ADYPEDResultReceiptNotPrinted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTerminalNotConfigured = (ADYPEDResultTerminalUnavailable + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelled = (ADYPEDResultTerminalNotConfigured + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultInvalidPIN = (ADYPEDResultShopperCancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPINTriesExceeded = (ADYPEDResultInvalidPIN + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPINValidationNotPossible = (ADYPEDResultPINTriesExceeded + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultWithdrawalAmountExceeded = (ADYPEDResultPINValidationNotPossible + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultWithdrawalCountExceeded = (ADYPEDResultWithdrawalAmountExceeded + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultFailedToGoOnline = (ADYPEDResultWithdrawalCountExceeded + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultDeclinedOffline = (ADYPEDResultFailedToGoOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPSPDeclined = (ADYPEDResultDeclinedOffline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultTransactionInterrupted = (ADYPEDResultPSPDeclined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCardSwapped = (ADYPEDResultTransactionInterrupted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultRiskManagementFailed = (ADYPEDResultCardSwapped + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPartiallyApproved = (ADYPEDResultRiskManagementFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCrashRecovery = (ADYPEDResultPartiallyApproved + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultIssuerReferral = (ADYPEDResultCrashRecovery + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultDeclinedOnline = (ADYPEDResultIssuerReferral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPrinterCancelled = (ADYPEDResultDeclinedOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultApplicationSelectionError = (ADYPEDResultPrinterCancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultCandidateListEmpty = (ADYPEDResultApplicationSelectionError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultPrinterTimedOut = (ADYPEDResultCandidateListEmpty + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledCtlsFallback = (ADYPEDResultPrinterTimedOut + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantCancelledCtlsFallback = (ADYPEDResultShopperCancelledCtlsFallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCardInsertTimedOutCtlsFallback = (ADYPEDResultMerchantCancelledCtlsFallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledAuthorizeOnline = (ADYPEDResultShopperCardInsertTimedOutCtlsFallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultShopperCancelledValidateOnline = (ADYPEDResultShopperCancelledAuthorizeOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantCancelledAuthorizeOnline = (ADYPEDResultShopperCancelledValidateOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantCancelledValidateOnline = (ADYPEDResultMerchantCancelledAuthorizeOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMerchantCancelledMke = (ADYPEDResultMerchantCancelledValidateOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMkeTimedOut = (ADYPEDResultMerchantCancelledMke + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultMOTONotAllowed = (ADYPEDResultMkeTimedOut + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

ADYPEDResultUnknown = (ADYPEDResultMOTONotAllowed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 82

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 91
if hasattr(_libs['adyen_pos'], 'get_number_of_ped_result_codes'):
    get_number_of_ped_result_codes = _libs['adyen_pos'].get_number_of_ped_result_codes
    get_number_of_ped_result_codes.argtypes = []
    get_number_of_ped_result_codes.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 94
if hasattr(_libs['adyen_pos'], 'get_ped_result_code_text'):
    get_ped_result_code_text = _libs['adyen_pos'].get_ped_result_code_text
    get_ped_result_code_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_ped_result_code_text.restype = ReturnString
    else:
        get_ped_result_code_text.restype = String
        get_ped_result_code_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 97
if hasattr(_libs['adyen_pos'], 'get_ped_result_code_enum'):
    get_ped_result_code_enum = _libs['adyen_pos'].get_ped_result_code_enum
    get_ped_result_code_enum.argtypes = [String]
    get_ped_result_code_enum.restype = ADYPEDResult

ADYPSPResultCode = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

enum_anon_4 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeOk = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeRegistered = (ADYPSPResultCodeOk + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeAlreadyRegistered = (ADYPSPResultCodeRegistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeProvided = (ADYPSPResultCodeAlreadyRegistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeRegistrationFailed = (ADYPSPResultCodeProvided + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeError = (ADYPSPResultCodeRegistrationFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeFailed = (ADYPSPResultCodeError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

ADYPSPResultCodeUnknown = (ADYPSPResultCodeFailed + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 104

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 117
if hasattr(_libs['adyen_pos'], 'get_number_of_PSP_codes'):
    get_number_of_PSP_codes = _libs['adyen_pos'].get_number_of_PSP_codes
    get_number_of_PSP_codes.argtypes = []
    get_number_of_PSP_codes.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 118
if hasattr(_libs['adyen_pos'], 'get_PSP_code_text'):
    get_PSP_code_text = _libs['adyen_pos'].get_PSP_code_text
    get_PSP_code_text.argtypes = [ADYPSPResultCode]
    if sizeof(c_int) == sizeof(c_void_p):
        get_PSP_code_text.restype = ReturnString
    else:
        get_PSP_code_text.restype = String
        get_PSP_code_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 119
if hasattr(_libs['adyen_pos'], 'get_PSP_code_enum'):
    get_PSP_code_enum = _libs['adyen_pos'].get_PSP_code_enum
    get_PSP_code_enum.argtypes = [String]
    get_PSP_code_enum.restype = ADYPSPResultCode

ADYEnvironment = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

enum_anon_5 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

ADYEnvironmentUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

ADYEnvironmentTest = (ADYEnvironmentUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

ADYEnvironmentLive = (ADYEnvironmentTest + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

ADYEnvironmentInvalid = (ADYEnvironmentLive + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 128

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 134
if hasattr(_libs['adyen_pos'], 'get_environment_text'):
    get_environment_text = _libs['adyen_pos'].get_environment_text
    get_environment_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_environment_text.restype = ReturnString
    else:
        get_environment_text.restype = String
        get_environment_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 135
if hasattr(_libs['adyen_pos'], 'get_environment_type_enum'):
    get_environment_type_enum = _libs['adyen_pos'].get_environment_type_enum
    get_environment_type_enum.argtypes = [String]
    get_environment_type_enum.restype = ADYEnvironment

ADYEventType = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

enum_anon_6 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeLogistic = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeLibStarted = (ADYEventTypeLogistic + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeDeviceConnected = (ADYEventTypeLibStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeDeviceBoarder = (ADYEventTypeDeviceConnected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeAppEvent = (ADYEventTypeDeviceBoarder + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeBoardingApp = (ADYEventTypeAppEvent + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeBoardingDevice = (ADYEventTypeBoardingApp + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTransactionStarted = (ADYEventTypeBoardingDevice + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTransactionCompletedApproved = (ADYEventTypeTransactionStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTransactionCompletedDeclined = (ADYEventTypeTransactionCompletedApproved + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTransactionCompletedCancelled = (ADYEventTypeTransactionCompletedDeclined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTransactionCompletedError = (ADYEventTypeTransactionCompletedCancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeRefundStarted = (ADYEventTypeTransactionCompletedError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeRefundScheduled = (ADYEventTypeRefundStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeRefundNotScheduled = (ADYEventTypeRefundScheduled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeMotoStarted = (ADYEventTypeRefundNotScheduled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeMotoScheduled = (ADYEventTypeMotoStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeMotoNotScheduled = (ADYEventTypeMotoScheduled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeBackgroundProcessStarted = (ADYEventTypeMotoNotScheduled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeBackgroundProcessCompleted = (ADYEventTypeBackgroundProcessStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTerminalUpdateReceivedFromPSP = (ADYEventTypeBackgroundProcessCompleted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeTerminalUpdatePushedToDevice = (ADYEventTypeTerminalUpdateReceivedFromPSP + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeSoftwareUpgradeReceivedFromPSP = (ADYEventTypeTerminalUpdatePushedToDevice + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeSoftwareUpgradeSoftwareUpgradePartialPushedToDevice = (ADYEventTypeSoftwareUpgradeReceivedFromPSP + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeSoftwareUpgradeSoftwareUpgradePushedToDevice = (ADYEventTypeSoftwareUpgradeSoftwareUpgradePartialPushedToDevice + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeException = (ADYEventTypeSoftwareUpgradeSoftwareUpgradePushedToDevice + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

ADYEventTypeVarious = (ADYEventTypeException + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 144

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 150
if hasattr(_libs['adyen_pos'], 'get_number_of_event_types'):
    get_number_of_event_types = _libs['adyen_pos'].get_number_of_event_types
    get_number_of_event_types.argtypes = []
    get_number_of_event_types.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 151
if hasattr(_libs['adyen_pos'], 'get_event_type_text'):
    get_event_type_text = _libs['adyen_pos'].get_event_type_text
    get_event_type_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_event_type_text.restype = ReturnString
    else:
        get_event_type_text.restype = String
        get_event_type_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 152
if hasattr(_libs['adyen_pos'], 'get_event_type_enum'):
    get_event_type_enum = _libs['adyen_pos'].get_event_type_enum
    get_event_type_enum.argtypes = [String]
    get_event_type_enum.restype = ADYEventType

ADYDataBody = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 157

enum_anon_7 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 157

ADYDataBodyNoConvert = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 157

ADYDataBodyXML = (ADYDataBodyNoConvert + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 157

ADYDataBodyJSON = (ADYDataBodyXML + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 157

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 162
if hasattr(_libs['adyen_pos'], 'get_data_body_string'):
    get_data_body_string = _libs['adyen_pos'].get_data_body_string
    get_data_body_string.argtypes = [ADYDataBody]
    if sizeof(c_int) == sizeof(c_void_p):
        get_data_body_string.restype = ReturnString
    else:
        get_data_body_string.restype = String
        get_data_body_string.errcheck = ReturnString

ADYIdentifyStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 173

enum_anon_8 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 173

ADYIdentifyStatusProvided = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 173

ADYIdentifyStatusError = 1 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 173

ADYIdentifyStatusUnknown = 3 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 173

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 182
if hasattr(_libs['adyen_pos'], 'get_number_of_identify_statuses'):
    get_number_of_identify_statuses = _libs['adyen_pos'].get_number_of_identify_statuses
    get_number_of_identify_statuses.argtypes = []
    get_number_of_identify_statuses.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 185
if hasattr(_libs['adyen_pos'], 'get_identify_status_text'):
    get_identify_status_text = _libs['adyen_pos'].get_identify_status_text
    get_identify_status_text.argtypes = [ADYIdentifyStatus]
    if sizeof(c_int) == sizeof(c_void_p):
        get_identify_status_text.restype = ReturnString
    else:
        get_identify_status_text.restype = String
        get_identify_status_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 188
if hasattr(_libs['adyen_pos'], 'get_identify_status_enum'):
    get_identify_status_enum = _libs['adyen_pos'].get_identify_status_enum
    get_identify_status_enum.argtypes = [String]
    get_identify_status_enum.restype = ADYIdentifyStatus

ADYSynchroniseStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 196

enum_anon_9 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 196

ADYSynchroniseStatusSuccessful = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 196

ADYSynchroniseStatusError = (ADYSynchroniseStatusSuccessful + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 196

ADYSynchroniseStatusUnknown = (ADYSynchroniseStatusError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 196

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 205
if hasattr(_libs['adyen_pos'], 'get_number_of_synchronise_statuses'):
    get_number_of_synchronise_statuses = _libs['adyen_pos'].get_number_of_synchronise_statuses
    get_number_of_synchronise_statuses.argtypes = []
    get_number_of_synchronise_statuses.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 208
if hasattr(_libs['adyen_pos'], 'get_synchronise_status_text'):
    get_synchronise_status_text = _libs['adyen_pos'].get_synchronise_status_text
    get_synchronise_status_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_synchronise_status_text.restype = ReturnString
    else:
        get_synchronise_status_text.restype = String
        get_synchronise_status_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 211
if hasattr(_libs['adyen_pos'], 'get_synchronise_status_enum'):
    get_synchronise_status_enum = _libs['adyen_pos'].get_synchronise_status_enum
    get_synchronise_status_enum.argtypes = [String]
    get_synchronise_status_enum.restype = ADYSynchroniseStatus

ADYCreateTenderStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

enum_anon_10 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

ADYCreateTenderStatusUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

ADYCreateTenderStatusCreated = (ADYCreateTenderStatusUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

ADYCreateTenderStatusError = (ADYCreateTenderStatusCreated + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

ADYCreateTenderUnfinishedTender = (ADYCreateTenderStatusError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

ADYCreateTenderRedirectShopper = (ADYCreateTenderUnfinishedTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 222

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 233
if hasattr(_libs['adyen_pos'], 'get_number_of_create_tender_statuses'):
    get_number_of_create_tender_statuses = _libs['adyen_pos'].get_number_of_create_tender_statuses
    get_number_of_create_tender_statuses.argtypes = []
    get_number_of_create_tender_statuses.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 236
if hasattr(_libs['adyen_pos'], 'get_create_tender_status_text'):
    get_create_tender_status_text = _libs['adyen_pos'].get_create_tender_status_text
    get_create_tender_status_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_create_tender_status_text.restype = ReturnString
    else:
        get_create_tender_status_text.restype = String
        get_create_tender_status_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 239
if hasattr(_libs['adyen_pos'], 'get_create_tender_status_enum'):
    get_create_tender_status_enum = _libs['adyen_pos'].get_create_tender_status_enum
    get_create_tender_status_enum.argtypes = [String]
    get_create_tender_status_enum.restype = ADYCreateTenderStatus

ADYUpdateTenderStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 250

enum_anon_11 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 250

ADYUpdateTenderStatusUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 250

ADYUpdateTenderStatusAccepted = (ADYUpdateTenderStatusUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 250

ADYUpdateTenderStatusFailed = (ADYUpdateTenderStatusAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 250

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 259
if hasattr(_libs['adyen_pos'], 'get_number_of_update_tender_statuses'):
    get_number_of_update_tender_statuses = _libs['adyen_pos'].get_number_of_update_tender_statuses
    get_number_of_update_tender_statuses.argtypes = []
    get_number_of_update_tender_statuses.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 262
if hasattr(_libs['adyen_pos'], 'get_update_tender_status_text'):
    get_update_tender_status_text = _libs['adyen_pos'].get_update_tender_status_text
    get_update_tender_status_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_update_tender_status_text.restype = ReturnString
    else:
        get_update_tender_status_text.restype = String
        get_update_tender_status_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 265
if hasattr(_libs['adyen_pos'], 'get_update_tender_status_enum'):
    get_update_tender_status_enum = _libs['adyen_pos'].get_update_tender_status_enum
    get_update_tender_status_enum.argtypes = [String]
    get_update_tender_status_enum.restype = ADYUpdateTenderStatus

ADYPaymentDeviceOption = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

enum_anon_12 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionInstallUpdateWhenAvailable = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionSynchroniseNow = (ADYPaymentDeviceOptionInstallUpdateWhenAvailable + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionCheckForUpdate = (ADYPaymentDeviceOptionSynchroniseNow + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionRestart = (ADYPaymentDeviceOptionCheckForUpdate + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionUnknown = (ADYPaymentDeviceOptionRestart + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionError = (ADYPaymentDeviceOptionUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

ADYPaymentDeviceOptionCount = (ADYPaymentDeviceOptionError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 274

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 287
if hasattr(_libs['adyen_pos'], 'get_number_of_payment_device_options'):
    get_number_of_payment_device_options = _libs['adyen_pos'].get_number_of_payment_device_options
    get_number_of_payment_device_options.argtypes = []
    get_number_of_payment_device_options.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 290
if hasattr(_libs['adyen_pos'], 'get_payment_device_option_text'):
    get_payment_device_option_text = _libs['adyen_pos'].get_payment_device_option_text
    get_payment_device_option_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_payment_device_option_text.restype = ReturnString
    else:
        get_payment_device_option_text.restype = String
        get_payment_device_option_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 293
if hasattr(_libs['adyen_pos'], 'get_payment_device_option_enum'):
    get_payment_device_option_enum = _libs['adyen_pos'].get_payment_device_option_enum
    get_payment_device_option_enum.argtypes = [String]
    get_payment_device_option_enum.restype = ADYPaymentDeviceOption

ADYTransactionType = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

enum_anon_13 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeNoChange = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeGoodsServices = (ADYTransactionTypeNoChange + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeGoodsServicesWithCashback = (ADYTransactionTypeGoodsServices + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeCash = (ADYTransactionTypeGoodsServicesWithCashback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeRefund = (ADYTransactionTypeCash + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeUnknown = (ADYTransactionTypeRefund + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

ADYTransactionTypeError = (ADYTransactionTypeUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 301

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 314
if hasattr(_libs['adyen_pos'], 'get_number_of_transaction_types'):
    get_number_of_transaction_types = _libs['adyen_pos'].get_number_of_transaction_types
    get_number_of_transaction_types.argtypes = []
    get_number_of_transaction_types.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 317
if hasattr(_libs['adyen_pos'], 'get_transaction_types_text'):
    get_transaction_types_text = _libs['adyen_pos'].get_transaction_types_text
    get_transaction_types_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_transaction_types_text.restype = ReturnString
    else:
        get_transaction_types_text.restype = String
        get_transaction_types_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 320
if hasattr(_libs['adyen_pos'], 'get_transaction_types_enum'):
    get_transaction_types_enum = _libs['adyen_pos'].get_transaction_types_enum
    get_transaction_types_enum.argtypes = [String]
    get_transaction_types_enum.restype = ADYTransactionType

ADYTenderOption = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

enum_anon_14 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionReceiptHandler = (ADYTenderOptionUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionGetAdditionalData = (ADYTenderOptionReceiptHandler + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionNoProcess = (ADYTenderOptionGetAdditionalData + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionKeyedEntry = (ADYTenderOptionNoProcess + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionBypassPIN = (ADYTenderOptionKeyedEntry + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionDontPrintReceipt = (ADYTenderOptionBypassPIN + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionAskGratuity = (ADYTenderOptionDontPrintReceipt + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionError = (ADYTenderOptionAskGratuity + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionForcedOnline = (ADYTenderOptionError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionForcedDecline = (ADYTenderOptionForcedOnline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionEnableMagstripeFallback = (ADYTenderOptionForcedDecline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionNoCTLS = (ADYTenderOptionEnableMagstripeFallback + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionAllowPartialAuthorisation = (ADYTenderOptionNoCTLS + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionTakeOverRunningTender = (ADYTenderOptionAllowPartialAuthorisation + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionAttendantActionHandler = (ADYTenderOptionTakeOverRunningTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionKeyedCardDetailsHandler = (ADYTenderOptionAttendantActionHandler + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionMOTO = (ADYTenderOptionKeyedCardDetailsHandler + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

ADYTenderOptionResultLast = (ADYTenderOptionMOTO + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 328

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 338
if hasattr(_libs['adyen_pos'], 'get_number_of_tender_options'):
    get_number_of_tender_options = _libs['adyen_pos'].get_number_of_tender_options
    get_number_of_tender_options.argtypes = []
    get_number_of_tender_options.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 341
if hasattr(_libs['adyen_pos'], 'get_tender_options_text'):
    get_tender_options_text = _libs['adyen_pos'].get_tender_options_text
    get_tender_options_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_tender_options_text.restype = ReturnString
    else:
        get_tender_options_text.restype = String
        get_tender_options_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 344
if hasattr(_libs['adyen_pos'], 'get_tender_options_enum'):
    get_tender_options_enum = _libs['adyen_pos'].get_tender_options_enum
    get_tender_options_enum.argtypes = [String]
    get_tender_options_enum.restype = ADYTenderOption

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 361
if hasattr(_libs['adyen_pos'], 'get_contract_name_enum_string'):
    get_contract_name_enum_string = _libs['adyen_pos'].get_contract_name_enum_string
    get_contract_name_enum_string.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_contract_name_enum_string.restype = ReturnString
    else:
        get_contract_name_enum_string.restype = String
        get_contract_name_enum_string.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 362
if hasattr(_libs['adyen_pos'], 'get_contract_names_text'):
    get_contract_names_text = _libs['adyen_pos'].get_contract_names_text
    get_contract_names_text.argtypes = [String, c_int, c_uint32]
    if sizeof(c_int) == sizeof(c_void_p):
        get_contract_names_text.restype = ReturnString
    else:
        get_contract_names_text.restype = String
        get_contract_names_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 363
if hasattr(_libs['adyen_pos'], 'get_contract_names_flags'):
    get_contract_names_flags = _libs['adyen_pos'].get_contract_names_flags
    get_contract_names_flags.argtypes = [String]
    get_contract_names_flags.restype = c_uint32

ADYTenderState = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

enum_anon_15 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateUndefined = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateAdditionalDataAvailable = (ADYTenderStateUndefined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStatePrintReceipt = (ADYTenderStateAdditionalDataAvailable + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCheckSignature = (ADYTenderStatePrintReceipt + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateAskDCC = (ADYTenderStateCheckSignature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateInitial = (ADYTenderStateAskDCC + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateTenderCreated = (ADYTenderStateInitial + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardInserted = (ADYTenderStateTenderCreated + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardSwiped = (ADYTenderStateCardInserted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateWaitForAppSelection = (ADYTenderStateCardSwiped + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateApplicationSelected = (ADYTenderStateWaitForAppSelection + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateWaitForAmountAdjustment = (ADYTenderStateApplicationSelected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateAskGratuity = (ADYTenderStateWaitForAmountAdjustment + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateGratuityEntered = (ADYTenderStateAskGratuity + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateDCCAccepted = (ADYTenderStateGratuityEntered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateDCCRejected = (ADYTenderStateDCCAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateProcessingTender = (ADYTenderStateDCCRejected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateWaitForPIN = (ADYTenderStateProcessingTender + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStatePINDigitEntered = (ADYTenderStateWaitForPIN + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStatePINEntered = (ADYTenderStatePINDigitEntered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateProvideCardDetails = (ADYTenderStatePINEntered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardDetailsProvided = (ADYTenderStateProvideCardDetails + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateReceiptPrinted = (ADYTenderStateCardDetailsProvided + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateReferralChecked = (ADYTenderStateReceiptPrinted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateSignatureChecked = (ADYTenderStateReferralChecked + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateAcknowledged = (ADYTenderStateSignatureChecked + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateReferral = (ADYTenderStateAcknowledged + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateAskSignature = (ADYTenderStateReferral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateApproved = (ADYTenderStateAskSignature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateDeclined = (ADYTenderStateApproved + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCancelled = (ADYTenderStateDeclined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateError = (ADYTenderStateCancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateBalaceQueryStarted = (ADYTenderStateError + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateBalaceQueryCompleted = (ADYTenderStateBalaceQueryStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateLoadStarted = (ADYTenderStateBalaceQueryCompleted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateBalaceQueryAcquired = (ADYTenderStateLoadStarted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateLoadCompleted = (ADYTenderStateBalaceQueryAcquired + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardMethodSelected = (ADYTenderStateLoadCompleted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardRemoved = (ADYTenderStateCardMethodSelected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateCardMKE = (ADYTenderStateCardRemoved + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateWaitForMKE = (ADYTenderStateCardMKE + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

ADYTenderStateUnknown = (ADYTenderStateWaitForMKE + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 374

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 383
if hasattr(_libs['adyen_pos'], 'get_number_of_tender_states'):
    get_number_of_tender_states = _libs['adyen_pos'].get_number_of_tender_states
    get_number_of_tender_states.argtypes = []
    get_number_of_tender_states.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 386
if hasattr(_libs['adyen_pos'], 'get_tender_state_text'):
    get_tender_state_text = _libs['adyen_pos'].get_tender_state_text
    get_tender_state_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_tender_state_text.restype = ReturnString
    else:
        get_tender_state_text.restype = String
        get_tender_state_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 389
if hasattr(_libs['adyen_pos'], 'get_tender_state_enum'):
    get_tender_state_enum = _libs['adyen_pos'].get_tender_state_enum
    get_tender_state_enum.argtypes = [String]
    get_tender_state_enum.restype = ADYTenderState

ADYReceiptLineFormat = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

enum_anon_16 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatNormal = (ADYReceiptLineFormatUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatEmphasis = (ADYReceiptLineFormatNormal + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatSignatureArea = (ADYReceiptLineFormatEmphasis + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImageBMP = (ADYReceiptLineFormatSignatureArea + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImageJPEG = (ADYReceiptLineFormatImageBMP + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImagePNG = (ADYReceiptLineFormatImageJPEG + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImageSVG = (ADYReceiptLineFormatImagePNG + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImage3BA = (ADYReceiptLineFormatImageSVG + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

ADYReceiptLineFormatImage4BA = (ADYReceiptLineFormatImage3BA + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 401

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 417
if hasattr(_libs['adyen_pos'], 'get_number_of_receipt_line_formats'):
    get_number_of_receipt_line_formats = _libs['adyen_pos'].get_number_of_receipt_line_formats
    get_number_of_receipt_line_formats.argtypes = []
    get_number_of_receipt_line_formats.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 420
if hasattr(_libs['adyen_pos'], 'get_receipt_line_format_text'):
    get_receipt_line_format_text = _libs['adyen_pos'].get_receipt_line_format_text
    get_receipt_line_format_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_receipt_line_format_text.restype = ReturnString
    else:
        get_receipt_line_format_text.restype = String
        get_receipt_line_format_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 423
if hasattr(_libs['adyen_pos'], 'get_receipt_line_format_enum'):
    get_receipt_line_format_enum = _libs['adyen_pos'].get_receipt_line_format_enum
    get_receipt_line_format_enum.argtypes = [String]
    get_receipt_line_format_enum.restype = ADYReceiptLineFormat

ADYUpdateTenderNewState = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

enum_anon_17 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateReceiptPrinted = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateCancel = (ADYUpdateTenderNewStateReceiptPrinted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateJustProcess = (ADYUpdateTenderNewStateCancel + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateAdjustAmount = (ADYUpdateTenderNewStateJustProcess + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateSignatureVerified = (ADYUpdateTenderNewStateAdjustAmount + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateReferral = (ADYUpdateTenderNewStateSignatureVerified + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateCancelCardOperation = (ADYUpdateTenderNewStateReferral + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateJustProcessCardOperation = (ADYUpdateTenderNewStateCancelCardOperation + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateAdjustAmountCardOperation = (ADYUpdateTenderNewStateJustProcessCardOperation + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

ADYUpdateTenderNewStateCardOperation = (ADYUpdateTenderNewStateAdjustAmountCardOperation + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 432

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 439
if hasattr(_libs['adyen_pos'], 'get_number_update_tender_states'):
    get_number_update_tender_states = _libs['adyen_pos'].get_number_update_tender_states
    get_number_update_tender_states.argtypes = []
    get_number_update_tender_states.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 440
if hasattr(_libs['adyen_pos'], 'update_tender_state_text'):
    update_tender_state_text = _libs['adyen_pos'].update_tender_state_text
    update_tender_state_text.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        update_tender_state_text.restype = ReturnString
    else:
        update_tender_state_text.restype = String
        update_tender_state_text.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 441
if hasattr(_libs['adyen_pos'], 'get_update_tender_enum'):
    get_update_tender_enum = _libs['adyen_pos'].get_update_tender_enum
    get_update_tender_enum.argtypes = [String]
    get_update_tender_enum.restype = ADYUpdateTenderNewState

ADYAttendantAction = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

enum_anon_18 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

ADYAttendantActionUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

ADYAttendantActionApproved = 1 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

ADYAttendantActionDeclined = 2 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

ADYAttendantActionRetry = 3 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 449

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 459
if hasattr(_libs['adyen_pos'], 'get_attendant_action_code_string'):
    get_attendant_action_code_string = _libs['adyen_pos'].get_attendant_action_code_string
    get_attendant_action_code_string.argtypes = [ADYAttendantAction]
    if sizeof(c_int) == sizeof(c_void_p):
        get_attendant_action_code_string.restype = ReturnString
    else:
        get_attendant_action_code_string.restype = String
        get_attendant_action_code_string.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 460
if hasattr(_libs['adyen_pos'], 'get_attendant_action_code_enum'):
    get_attendant_action_code_enum = _libs['adyen_pos'].get_attendant_action_code_enum
    get_attendant_action_code_enum.argtypes = [String]
    get_attendant_action_code_enum.restype = ADYAttendantAction

ADYPEDState = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

enum_anon_19 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateUndetected = 0 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateDetected = (ADYPEDStateUndetected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateUnregistered = (ADYPEDStateDetected + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateIdentified = (ADYPEDStateUnregistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateRegistered = (ADYPEDStateIdentified + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateConfigSynced = (ADYPEDStateRegistered + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateWaitRebootReady = (ADYPEDStateConfigSynced + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateWaitReadyForTransaction = (ADYPEDStateWaitRebootReady + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateNotReady = (ADYPEDStateWaitReadyForTransaction + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateReadyForTransaction = (ADYPEDStateNotReady + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

ADYPEDStateTender = (ADYPEDStateReadyForTransaction + 1) # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 468

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 474
if hasattr(_libs['adyen_pos'], 'get_number_ped_states'):
    get_number_ped_states = _libs['adyen_pos'].get_number_ped_states
    get_number_ped_states.argtypes = []
    get_number_ped_states.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 475
if hasattr(_libs['adyen_pos'], 'get_ped_state_string'):
    get_ped_state_string = _libs['adyen_pos'].get_ped_state_string
    get_ped_state_string.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        get_ped_state_string.restype = ReturnString
    else:
        get_ped_state_string.restype = String
        get_ped_state_string.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 476
if hasattr(_libs['adyen_pos'], 'get_ped_state_enum'):
    get_ped_state_enum = _libs['adyen_pos'].get_ped_state_enum
    get_ped_state_enum.argtypes = [String]
    get_ped_state_enum.restype = ADYPEDState

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 477
if hasattr(_libs['adyen_pos'], 'get_system_platform_str'):
    get_system_platform_str = _libs['adyen_pos'].get_system_platform_str
    get_system_platform_str.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        get_system_platform_str.restype = ReturnString
    else:
        get_system_platform_str.restype = String
        get_system_platform_str.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 484
class struct_anon_20(Structure):
    pass

struct_anon_20.__slots__ = [
    'library_result_code',
    'psp_result_code',
    'ped_result_code',
    'error_message',
]
struct_anon_20._fields_ = [
    ('library_result_code', ADYLibraryResult),
    ('psp_result_code', ADYPSPResultCode),
    ('ped_result_code', ADYPEDResult),
    ('error_message', String),
]

ADYEN_RESULT = struct_anon_20 # /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 484

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 487
if hasattr(_libs['adyen_pos'], 'get_error_code_by_int'):
    get_error_code_by_int = _libs['adyen_pos'].get_error_code_by_int
    get_error_code_by_int.argtypes = [c_int]
    get_error_code_by_int.restype = ADYPEDResult

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 488
if hasattr(_libs['adyen_pos'], 'get_error_code_by_str'):
    get_error_code_by_str = _libs['adyen_pos'].get_error_code_by_str
    get_error_code_by_str.argtypes = [String]
    get_error_code_by_str.restype = ADYPEDResult

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 489
if hasattr(_libs['adyen_pos'], 'get_error_code_by_ped_result_code'):
    get_error_code_by_ped_result_code = _libs['adyen_pos'].get_error_code_by_ped_result_code
    get_error_code_by_ped_result_code.argtypes = [ADYPEDResult]
    get_error_code_by_ped_result_code.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 490
if hasattr(_libs['adyen_pos'], 'get_decline_code'):
    get_decline_code = _libs['adyen_pos'].get_decline_code
    get_decline_code.argtypes = [String, ADYPEDResult]
    get_decline_code.restype = ADYPEDResult

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 18
class struct_anon_44(Structure):
    pass

struct_anon_44.__slots__ = [
    'key',
    'value',
]
struct_anon_44._fields_ = [
    ('key', String),
    ('value', String),
]

additional_data_kvp = struct_anon_44 # /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 18

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 24
class struct_anon_45(Structure):
    pass

struct_anon_45.__slots__ = [
    'pre_alloc_size',
    'size',
    'AD',
]
struct_anon_45._fields_ = [
    ('pre_alloc_size', c_int),
    ('size', c_int),
    ('AD', POINTER(POINTER(additional_data_kvp))),
]

additional_data_struct = struct_anon_45 # /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 24

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 27
if hasattr(_libs['adyen_pos'], 'additional_data_obj_allocate'):
    additional_data_obj_allocate = _libs['adyen_pos'].additional_data_obj_allocate
    additional_data_obj_allocate.argtypes = []
    additional_data_obj_allocate.restype = POINTER(additional_data_struct)

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 28
if hasattr(_libs['adyen_pos'], 'get_additional_data_size'):
    get_additional_data_size = _libs['adyen_pos'].get_additional_data_size
    get_additional_data_size.argtypes = [POINTER(additional_data_struct)]
    get_additional_data_size.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 29
if hasattr(_libs['adyen_pos'], 'get_additional_data_kvp_value'):
    get_additional_data_kvp_value = _libs['adyen_pos'].get_additional_data_kvp_value
    get_additional_data_kvp_value.argtypes = [POINTER(additional_data_struct), String]
    if sizeof(c_int) == sizeof(c_void_p):
        get_additional_data_kvp_value.restype = ReturnString
    else:
        get_additional_data_kvp_value.restype = String
        get_additional_data_kvp_value.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 30
if hasattr(_libs['adyen_pos'], 'add_additional_data_kvp'):
    add_additional_data_kvp = _libs['adyen_pos'].add_additional_data_kvp
    add_additional_data_kvp.argtypes = [POINTER(additional_data_struct), String, String]
    add_additional_data_kvp.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 31
if hasattr(_libs['adyen_pos'], 'reset_additional_data_obj'):
    reset_additional_data_obj = _libs['adyen_pos'].reset_additional_data_obj
    reset_additional_data_obj.argtypes = [POINTER(additional_data_struct)]
    reset_additional_data_obj.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 32
if hasattr(_libs['adyen_pos'], 'set_additional_data_kvp_by_id'):
    set_additional_data_kvp_by_id = _libs['adyen_pos'].set_additional_data_kvp_by_id
    set_additional_data_kvp_by_id.argtypes = [POINTER(additional_data_struct), c_int, String, String]
    set_additional_data_kvp_by_id.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 33
if hasattr(_libs['adyen_pos'], 'get_additional_data_kvp_by_id'):
    get_additional_data_kvp_by_id = _libs['adyen_pos'].get_additional_data_kvp_by_id
    get_additional_data_kvp_by_id.argtypes = [POINTER(additional_data_struct), c_int, POINTER(POINTER(c_char)), POINTER(POINTER(c_char))]
    get_additional_data_kvp_by_id.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/additional_data_obj.h: 34
if hasattr(_libs['adyen_pos'], 'iterate_additional_data'):
    iterate_additional_data = _libs['adyen_pos'].iterate_additional_data
    iterate_additional_data.argtypes = [POINTER(additional_data_struct), CFUNCTYPE(UNCHECKED(None), c_int, String, String, POINTER(None)), POINTER(None)]
    iterate_additional_data.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 19
class struct_anon_46(Structure):
    pass

struct_anon_46.__slots__ = [
    'size',
    'options',
]
struct_anon_46._fields_ = [
    ('size', c_int),
    ('options', ADYTenderOption * ADYTenderOptionResultLast),
]

tender_options_struct = struct_anon_46 # /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 19

# /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 22
if hasattr(_libs['adyen_pos'], 'tender_options_obj_allocate'):
    tender_options_obj_allocate = _libs['adyen_pos'].tender_options_obj_allocate
    tender_options_obj_allocate.argtypes = []
    tender_options_obj_allocate.restype = POINTER(tender_options_struct)

# /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 23
if hasattr(_libs['adyen_pos'], 'test_tender_option'):
    test_tender_option = _libs['adyen_pos'].test_tender_option
    test_tender_option.argtypes = [POINTER(tender_options_struct), ADYTenderOption]
    test_tender_option.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 24
if hasattr(_libs['adyen_pos'], 'rm_tender_option'):
    rm_tender_option = _libs['adyen_pos'].rm_tender_option
    rm_tender_option.argtypes = [POINTER(tender_options_struct), ADYTenderOption]
    rm_tender_option.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/tender_options_obj.h: 25
if hasattr(_libs['adyen_pos'], 'add_tender_option'):
    add_tender_option = _libs['adyen_pos'].add_tender_option
    add_tender_option.argtypes = [POINTER(tender_options_struct), ADYTenderOption]
    add_tender_option.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 40
class struct_anon_47(Structure):
    pass

struct_anon_47.__slots__ = [
    'ped',
    'merchant_account',
    'terminal_id',
    'card_type',
    'card_number',
    'expiry_month',
    'expiry_year',
    'card_mask',
    'card_mask_min',
    'card_mask_max',
    'reference',
    'tender_options_obj',
    'additional_data_obj',
]
struct_anon_47._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('terminal_id', String),
    ('card_type', String),
    ('card_number', String),
    ('expiry_month', c_int),
    ('expiry_year', c_int),
    ('card_mask', String),
    ('card_mask_min', c_int),
    ('card_mask_max', c_int),
    ('reference', String),
    ('tender_options_obj', POINTER(tender_options_struct)),
    ('additional_data_obj', POINTER(additional_data_struct)),
]

balance_inquiry_request = struct_anon_47 # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 40

ADYBalanceInquiryStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 43

enum_anon_48 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 43

ADYLibraryBalanceInquiryUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 43

ADYLibraryBalanceAccepted = (ADYLibraryBalanceInquiryUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 43

ADYLibraryBalanceInquiryFailed = (ADYLibraryBalanceAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 43

# /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 53
class struct_anon_49(Structure):
    pass

struct_anon_49.__slots__ = [
    'parsed_result',
    'tender_reference',
]
struct_anon_49._fields_ = [
    ('parsed_result', ADYEN_RESULT),
    ('tender_reference', String),
]

balance_inquiry_response = struct_anon_49 # /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 53

# /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 55
if hasattr(_libs['adyen_pos'], 'balance_inquiry_allocate'):
    balance_inquiry_allocate = _libs['adyen_pos'].balance_inquiry_allocate
    balance_inquiry_allocate.argtypes = []
    balance_inquiry_allocate.restype = POINTER(balance_inquiry_request)

# /home/app/pywebdriver/adyen/linux/lib_include/balance_inquiry_extern.h: 56
if hasattr(_libs['adyen_pos'], 'balance_inquiry'):
    balance_inquiry = _libs['adyen_pos'].balance_inquiry
    balance_inquiry.argtypes = [POINTER(balance_inquiry_request), CFUNCTYPE(UNCHECKED(None), POINTER(balance_inquiry_response), POINTER(None)), POINTER(None)]
    balance_inquiry.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 26
class struct_anon_50(Structure):
    pass

struct_anon_50.__slots__ = [
    'merchant_account',
    'reference',
    'original_reference',
    'tender_reference',
    'unique_terminal_id',
]
struct_anon_50._fields_ = [
    ('merchant_account', String),
    ('reference', String),
    ('original_reference', String),
    ('tender_reference', String),
    ('unique_terminal_id', String),
]

cancel_or_refund_request = struct_anon_50 # /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 26

# /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 33
class struct_anon_51(Structure):
    pass

struct_anon_51.__slots__ = [
    'cancel_or_refund_request_ptr',
    'psp_reference',
    'response',
    'parsed_result',
]
struct_anon_51._fields_ = [
    ('cancel_or_refund_request_ptr', POINTER(cancel_or_refund_request)),
    ('psp_reference', String),
    ('response', String),
    ('parsed_result', ADYEN_RESULT),
]

cancel_or_refund_response = struct_anon_51 # /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 33

# /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 37
if hasattr(_libs['adyen_pos'], 'cancel_or_refund'):
    cancel_or_refund = _libs['adyen_pos'].cancel_or_refund
    cancel_or_refund.argtypes = [POINTER(cancel_or_refund_request), CFUNCTYPE(UNCHECKED(None), POINTER(cancel_or_refund_response), POINTER(None)), POINTER(None)]
    cancel_or_refund.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/cancel_or_refund_extern.h: 38
if hasattr(_libs['adyen_pos'], 'cancel_or_refund_allocate'):
    cancel_or_refund_allocate = _libs['adyen_pos'].cancel_or_refund_allocate
    cancel_or_refund_allocate.argtypes = []
    cancel_or_refund_allocate.restype = POINTER(cancel_or_refund_request)

# /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 30
class struct_anon_52(Structure):
    pass

struct_anon_52.__slots__ = [
    'ped',
    'merchant_account',
    'terminal_id',
    'tender_reference',
    'card_type',
    'card_number',
    'expiry_month',
    'expiry_year',
    'card_mask',
    'card_mask_min',
    'card_mask_max',
    'additional_data_obj',
]
struct_anon_52._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('terminal_id', String),
    ('tender_reference', String),
    ('card_type', String),
    ('card_number', String),
    ('expiry_month', c_int),
    ('expiry_year', c_int),
    ('card_mask', String),
    ('card_mask_min', c_int),
    ('card_mask_max', c_int),
    ('additional_data_obj', POINTER(additional_data_struct)),
]

card_operation_request = struct_anon_52 # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 30

ADYCardOperationStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 33

enum_anon_53 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 33

ADYLibraryCardOperationUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 33

ADYLibraryCardOperationAccepted = (ADYLibraryCardOperationUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 33

ADYLibraryCardOperationFailed = (ADYLibraryCardOperationAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 33

# /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 42
if hasattr(_libs['adyen_pos'], 'card_operation_allocate'):
    card_operation_allocate = _libs['adyen_pos'].card_operation_allocate
    card_operation_allocate.argtypes = []
    card_operation_allocate.restype = POINTER(card_operation_request)

# /home/app/pywebdriver/adyen/linux/lib_include/card_operation_request.h: 43
if hasattr(_libs['adyen_pos'], 'card_operation'):
    card_operation = _libs['adyen_pos'].card_operation
    card_operation.argtypes = [POINTER(card_operation_request)]
    card_operation.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 38
class struct_anon_54(Structure):
    pass

struct_anon_54.__slots__ = [
    'ped',
    'merchant_account',
    'transaction_type',
    'reference',
    'order_reference',
    'terminal_id',
    'amount_currency',
    'amount_value',
    'gratuity_amount_currency',
    'gratuity_amount_value',
    'shopper_email',
    'shopper_reference',
    'recurring_contract',
    'recurring_contract_detail_name',
    'tender_options_obj',
    'additional_data_obj',
]
struct_anon_54._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('transaction_type', ADYTransactionType),
    ('reference', String),
    ('order_reference', String),
    ('terminal_id', String),
    ('amount_currency', String),
    ('amount_value', c_long),
    ('gratuity_amount_currency', String),
    ('gratuity_amount_value', c_long),
    ('shopper_email', String),
    ('shopper_reference', String),
    ('recurring_contract', String),
    ('recurring_contract_detail_name', String),
    ('tender_options_obj', POINTER(tender_options_struct)),
    ('additional_data_obj', POINTER(additional_data_struct)),
]

create_tender_request = struct_anon_54 # /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 38

# /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 45
class struct_anon_55(Structure):
    pass

struct_anon_55.__slots__ = [
    'terminal_id',
    'tender_reference',
    'create_tender_status',
    'parsed_result',
]
struct_anon_55._fields_ = [
    ('terminal_id', String),
    ('tender_reference', String),
    ('create_tender_status', ADYCreateTenderStatus),
    ('parsed_result', ADYEN_RESULT),
]

create_tender_response = struct_anon_55 # /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 45

# /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 47
if hasattr(_libs['adyen_pos'], 'create_tender_allocate'):
    create_tender_allocate = _libs['adyen_pos'].create_tender_allocate
    create_tender_allocate.argtypes = []
    create_tender_allocate.restype = POINTER(create_tender_request)

# /home/app/pywebdriver/adyen/linux/lib_include/create_tender_extern.h: 48
if hasattr(_libs['adyen_pos'], 'create_tender'):
    create_tender = _libs['adyen_pos'].create_tender
    create_tender.argtypes = [POINTER(create_tender_request), CFUNCTYPE(UNCHECKED(None), POINTER(create_tender_response), POINTER(None)), POINTER(None)]
    create_tender.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 34
class struct_anon_56(Structure):
    pass

struct_anon_56.__slots__ = [
    'ped',
    'special_options',
    'handle_receipt',
    'terminal_id',
    'merchant_account',
    'reference',
    'transaction_type',
    'payment_method_type',
    'amount_currency',
    'amount_value',
    'additional_data',
]
struct_anon_56._fields_ = [
    ('ped', POINTER(None)),
    ('special_options', POINTER(None)),
    ('handle_receipt', c_bool),
    ('terminal_id', String),
    ('merchant_account', String),
    ('reference', String),
    ('transaction_type', String),
    ('payment_method_type', String),
    ('amount_currency', String),
    ('amount_value', c_long),
    ('additional_data', POINTER(additional_data_struct)),
]

special_tender_request = struct_anon_56 # /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 34

# /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 36
if hasattr(_libs['adyen_pos'], 'create_special_tender'):
    create_special_tender = _libs['adyen_pos'].create_special_tender
    create_special_tender.argtypes = [POINTER(special_tender_request), CFUNCTYPE(UNCHECKED(None), POINTER(create_tender_response), POINTER(None)), POINTER(None)]
    create_special_tender.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 37
if hasattr(_libs['adyen_pos'], 'special_tender_add_option'):
    special_tender_add_option = _libs['adyen_pos'].special_tender_add_option
    special_tender_add_option.argtypes = [POINTER(special_tender_request), String, String]
    special_tender_add_option.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 38
if hasattr(_libs['adyen_pos'], 'special_tender_rm_option'):
    special_tender_rm_option = _libs['adyen_pos'].special_tender_rm_option
    special_tender_rm_option.argtypes = [POINTER(special_tender_request), String]
    special_tender_rm_option.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/create_special_tender_extern.h: 39
if hasattr(_libs['adyen_pos'], 'create_special_tender_request'):
    create_special_tender_request = _libs['adyen_pos'].create_special_tender_request
    create_special_tender_request.argtypes = []
    create_special_tender_request.restype = POINTER(special_tender_request)

# /home/app/pywebdriver/adyen/linux/lib_include/ped_device_info.h: 48
class struct_anon_57(Structure):
    pass

struct_anon_57.__slots__ = [
    'device_state',
    'terminal_id',
    'terminal_serial_number',
    'terminal_type',
    'terminal_brand',
    'terminal_api_version',
    'terminal_os_version',
    'terminal_hardware_version',
    'batteryPercentage',
    'ready_for_tender',
    'tender_reference',
    'additional_data_obj',
    'result',
    'last_updated',
    'external_reference',
]
struct_anon_57._fields_ = [
    ('device_state', ADYPEDState),
    ('terminal_id', String),
    ('terminal_serial_number', String),
    ('terminal_type', String),
    ('terminal_brand', String),
    ('terminal_api_version', String),
    ('terminal_os_version', String),
    ('terminal_hardware_version', String),
    ('batteryPercentage', c_int),
    ('ready_for_tender', c_int),
    ('tender_reference', String),
    ('additional_data_obj', POINTER(additional_data_struct)),
    ('result', ADYEN_RESULT),
    ('last_updated', c_longlong),
    ('external_reference', POINTER(None)),
]

ped_device_info = struct_anon_57 # /home/app/pywebdriver/adyen/linux/lib_include/ped_device_info.h: 48

# /home/app/pywebdriver/adyen/linux/lib_include/ped_device_info.h: 50
if hasattr(_libs['adyen_pos'], 'ped_device_info_to_string'):
    ped_device_info_to_string = _libs['adyen_pos'].ped_device_info_to_string
    ped_device_info_to_string.argtypes = [String, c_int, POINTER(None)]
    ped_device_info_to_string.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/ped_device_info.h: 52
if hasattr(_libs['adyen_pos'], 'get_ped_info_indexed'):
    get_ped_info_indexed = _libs['adyen_pos'].get_ped_info_indexed
    get_ped_info_indexed.argtypes = [c_int]
    get_ped_info_indexed.restype = POINTER(ped_device_info)

# /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 23
class struct_anon_58(Structure):
    pass

struct_anon_58.__slots__ = [
    'line_key',
    'position',
    'name',
    'abbreviation',
    'value',
    'format',
]
struct_anon_58._fields_ = [
    ('line_key', String),
    ('position', c_int),
    ('name', String),
    ('abbreviation', String),
    ('value', String),
    ('format', ADYReceiptLineFormat),
]

receipt_line = struct_anon_58 # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 23

# /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 34
class struct_anon_59(Structure):
    pass

struct_anon_59.__slots__ = [
    'number_of_header_lines',
    'header',
    'number_of_content_lines',
    'content',
    'number_of_footer_lines',
    'footer',
]
struct_anon_59._fields_ = [
    ('number_of_header_lines', c_int),
    ('header', POINTER(POINTER(receipt_line))),
    ('number_of_content_lines', c_int),
    ('content', POINTER(POINTER(receipt_line))),
    ('number_of_footer_lines', c_int),
    ('footer', POINTER(POINTER(receipt_line))),
]

receipt = struct_anon_59 # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 34

enum_anon_60 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_undefined = 0 # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_authorised = (receipt_type_undefined + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_refused = (receipt_type_authorised + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_signature = (receipt_type_refused + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_cancelled = (receipt_type_signature + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_refund_authorised = (receipt_type_cancelled + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type_refund_refused = (receipt_type_refund_authorised + 1) # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

receipt_type = enum_anon_60 # /home/app/pywebdriver/adyen/linux/lib_include/receipt_data_obj.h: 44

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 27
class struct_anon_61(Structure):
    pass

struct_anon_61.__slots__ = [
    'internal_ped_object',
    'terminal_id',
    'tender_reference',
    'additional_data_obj',
    'state',
    'parsed_result',
]
struct_anon_61._fields_ = [
    ('internal_ped_object', POINTER(None)),
    ('terminal_id', String),
    ('tender_reference', String),
    ('additional_data_obj', POINTER(additional_data_struct)),
    ('state', ADYTenderState),
    ('parsed_result', ADYEN_RESULT),
]

response_header = struct_anon_61 # /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 27

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 36
class struct_anon_62(Structure):
    pass

struct_anon_62.__slots__ = [
    'info',
    'merchant_receipt',
    'card_holder_receipt',
    'type',
]
struct_anon_62._fields_ = [
    ('info', response_header),
    ('merchant_receipt', receipt),
    ('card_holder_receipt', receipt),
    ('type', receipt_type),
]

receipts_strct = struct_anon_62 # /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 36

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 43
class struct_anon_63(Structure):
    pass

struct_anon_63.__slots__ = [
    'info',
    'auth_code',
    'refusal_reason',
    'result_code',
]
struct_anon_63._fields_ = [
    ('info', response_header),
    ('auth_code', String),
    ('refusal_reason', String),
    ('result_code', String),
]

final_strct = struct_anon_63 # /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 43

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 49
class union_anon_64(Union):
    pass

union_anon_64.__slots__ = [
    'header',
    'receipts',
    'final',
]
union_anon_64._fields_ = [
    ('header', response_header),
    ('receipts', receipts_strct),
    ('final', final_strct),
]

union_data = union_anon_64 # /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 49

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 55
class struct_anon_65(Structure):
    pass

struct_anon_65.__slots__ = [
    'data',
    'state',
    'stateSequenceNumber',
]
struct_anon_65._fields_ = [
    ('data', union_data),
    ('state', POINTER(ped_device_info)),
    ('stateSequenceNumber', c_longlong),
]

status_tender_merged_response = struct_anon_65 # /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 55

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 58
if hasattr(_libs['adyen_pos'], 'receipt_type_to_string'):
    receipt_type_to_string = _libs['adyen_pos'].receipt_type_to_string
    receipt_type_to_string.argtypes = [receipt_type]
    if sizeof(c_int) == sizeof(c_void_p):
        receipt_type_to_string.restype = ReturnString
    else:
        receipt_type_to_string.restype = String
        receipt_type_to_string.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/status_tender_response.h: 59
if hasattr(_libs['adyen_pos'], 'receipt_type_to_enum'):
    receipt_type_to_enum = _libs['adyen_pos'].receipt_type_to_enum
    receipt_type_to_enum.argtypes = [String]
    receipt_type_to_enum.restype = receipt_type

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 44
class struct_anon_66(Structure):
    pass

struct_anon_66.__slots__ = [
    'libraryRetainsVariables',
    'flags',
    'library_log',
    'library_log_echo',
    'environment',
    'pos_name',
    'app_name',
    'app_id',
    'integrator_name',
    'throw_exception',
    'echo_struct',
    'logArea',
    'PAL_URL',
    'CA_URL',
    'thread_startup_procedure',
    'backend_use_proxy',
]
struct_anon_66._fields_ = [
    ('libraryRetainsVariables', c_int),
    ('flags', c_uint32),
    ('library_log', CFUNCTYPE(UNCHECKED(None), String, String)),
    ('library_log_echo', CFUNCTYPE(UNCHECKED(None), String, String, POINTER(None))),
    ('environment', ADYEnvironment),
    ('pos_name', String),
    ('app_name', String),
    ('app_id', String),
    ('integrator_name', String),
    ('throw_exception', CFUNCTYPE(UNCHECKED(None), POINTER(final_strct), POINTER(ped_device_info), POINTER(None))),
    ('echo_struct', POINTER(None)),
    ('logArea', c_uint32),
    ('PAL_URL', String),
    ('CA_URL', String),
    ('thread_startup_procedure', CFUNCTYPE(UNCHECKED(None), )),
    ('backend_use_proxy', String),
]

init_library_request = struct_anon_66 # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 44

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 50
if hasattr(_libs['adyen_pos'], 'init_library'):
    init_library = _libs['adyen_pos'].init_library
    init_library.argtypes = [POINTER(init_library_request), CFUNCTYPE(UNCHECKED(None), POINTER(None), POINTER(None)), POINTER(None)]
    init_library.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 51
if hasattr(_libs['adyen_pos'], 'exit_task'):
    exit_task = _libs['adyen_pos'].exit_task
    exit_task.argtypes = [CFUNCTYPE(UNCHECKED(None), POINTER(None), POINTER(None)), POINTER(None)]
    exit_task.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 52
if hasattr(_libs['adyen_pos'], 'get_peds_count'):
    get_peds_count = _libs['adyen_pos'].get_peds_count
    get_peds_count.argtypes = []
    get_peds_count.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 53
if hasattr(_libs['adyen_pos'], 'get_library_state'):
    get_library_state = _libs['adyen_pos'].get_library_state
    get_library_state.argtypes = []
    get_library_state.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 54
if hasattr(_libs['adyen_pos'], 'set_library_echo_struct'):
    set_library_echo_struct = _libs['adyen_pos'].set_library_echo_struct
    set_library_echo_struct.argtypes = [POINTER(None)]
    set_library_echo_struct.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 55
if hasattr(_libs['adyen_pos'], 'query_ped_state'):
    query_ped_state = _libs['adyen_pos'].query_ped_state
    query_ped_state.argtypes = [String, c_int]
    query_ped_state.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 56
if hasattr(_libs['adyen_pos'], 'init_library_allocate'):
    init_library_allocate = _libs['adyen_pos'].init_library_allocate
    init_library_allocate.argtypes = []
    init_library_allocate.restype = POINTER(init_library_request)

enum_anon_67 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 61

library_network_state_offline = 0 # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 61

library_network_state_online = (library_network_state_offline + 1) # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 61

enum_library_network_state = enum_anon_67 # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 61

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 63
if hasattr(_libs['adyen_pos'], 'set_library_network_state'):
    set_library_network_state = _libs['adyen_pos'].set_library_network_state
    set_library_network_state.argtypes = [enum_library_network_state]
    set_library_network_state.restype = ADYLibraryResult

enum_anon_68 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 69

enum_lib_unit_pipes = 0 # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 69

enum_lib_unit_websockets = (enum_lib_unit_pipes + 1) # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 69

enum_lib_unit = enum_anon_68 # /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 69

# /home/app/pywebdriver/adyen/linux/lib_include/library_extern.h: 70
if hasattr(_libs['adyen_pos'], 'do_library_unit_test'):
    do_library_unit_test = _libs['adyen_pos'].do_library_unit_test
    do_library_unit_test.argtypes = [enum_lib_unit]
    do_library_unit_test.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 46
class struct_anon_69(Structure):
    pass

struct_anon_69.__slots__ = [
    'ped',
    'merchant_account',
    'terminal_id',
    'card_type',
    'load_type',
    'amount_currency',
    'amount_value',
    'card_number',
    'expiry_month',
    'expiry_year',
    'card_mask',
    'card_mask_min',
    'card_mask_max',
    'reference',
    'tender_options_obj',
    'additional_data_obj',
]
struct_anon_69._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('terminal_id', String),
    ('card_type', String),
    ('load_type', String),
    ('amount_currency', String),
    ('amount_value', c_long),
    ('card_number', String),
    ('expiry_month', c_int),
    ('expiry_year', c_int),
    ('card_mask', String),
    ('card_mask_min', c_int),
    ('card_mask_max', c_int),
    ('reference', String),
    ('tender_options_obj', POINTER(tender_options_struct)),
    ('additional_data_obj', POINTER(additional_data_struct)),
]

load_request = struct_anon_69 # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 46

ADYLoadStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 49

enum_anon_70 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 49

ADYLibraryLoadUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 49

ADYLibraryLoadAccepted = (ADYLibraryLoadUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 49

ADYLibraryLoadFailed = (ADYLibraryLoadAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 49

# /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 61
class struct_anon_71(Structure):
    pass

struct_anon_71.__slots__ = [
    'terminal_id',
    'tender_reference',
    'load_card_staus',
    'parsed_result',
]
struct_anon_71._fields_ = [
    ('terminal_id', String),
    ('tender_reference', String),
    ('load_card_staus', ADYLoadStatus),
    ('parsed_result', ADYEN_RESULT),
]

load_request_response = struct_anon_71 # /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 61

# /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 67
if hasattr(_libs['adyen_pos'], 'load_allocate'):
    load_allocate = _libs['adyen_pos'].load_allocate
    load_allocate.argtypes = []
    load_allocate.restype = POINTER(load_request)

# /home/app/pywebdriver/adyen/linux/lib_include/load_request_extern.h: 68
if hasattr(_libs['adyen_pos'], 'load'):
    load = _libs['adyen_pos'].load
    load.argtypes = [POINTER(load_request), CFUNCTYPE(UNCHECKED(None), POINTER(load_request_response), POINTER(None)), POINTER(None)]
    load.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/obj_manager.h: 23
if hasattr(_libs['adyen_pos'], 'check_reference_obj'):
    check_reference_obj = _libs['adyen_pos'].check_reference_obj
    check_reference_obj.argtypes = [POINTER(None)]
    check_reference_obj.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/obj_manager.h: 29
if hasattr(_libs['adyen_pos'], '_release_reference_obj'):
    _release_reference_obj = _libs['adyen_pos']._release_reference_obj
    _release_reference_obj.argtypes = [POINTER(None), String, c_int]
    _release_reference_obj.restype = None

# /home/app/pywebdriver/adyen/linux/lib_include/obj_manager.h: 34
if hasattr(_libs['adyen_pos'], '_retain_reference_obj'):
    _retain_reference_obj = _libs['adyen_pos']._retain_reference_obj
    _retain_reference_obj.argtypes = [POINTER(None), String, c_int]
    _retain_reference_obj.restype = POINTER(None)

# /home/app/pywebdriver/adyen/linux/lib_include/obj_manager.h: 37
if hasattr(_libs['adyen_pos'], '_set_reference_obj'):
    _set_reference_obj = _libs['adyen_pos']._set_reference_obj
    _set_reference_obj.argtypes = [POINTER(POINTER(None)), POINTER(None), String, c_int]
    _set_reference_obj.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 29
class struct_anon_72(Structure):
    pass

struct_anon_72.__slots__ = [
    'merchant_account',
    'reference',
    'psp_reference',
    'tender_reference',
    'unique_terminal_id',
    'modification_amount_currency',
    'modification_amount_value',
]
struct_anon_72._fields_ = [
    ('merchant_account', String),
    ('reference', String),
    ('psp_reference', String),
    ('tender_reference', String),
    ('unique_terminal_id', String),
    ('modification_amount_currency', String),
    ('modification_amount_value', c_long),
]

refund_request = struct_anon_72 # /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 29

# /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 36
class struct_anon_73(Structure):
    pass

struct_anon_73.__slots__ = [
    'refund_request_ptr',
    'psp_reference',
    'response',
    'parsed_result',
]
struct_anon_73._fields_ = [
    ('refund_request_ptr', POINTER(refund_request)),
    ('psp_reference', String),
    ('response', String),
    ('parsed_result', ADYEN_RESULT),
]

refund_response = struct_anon_73 # /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 36

# /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 40
if hasattr(_libs['adyen_pos'], 'refund'):
    refund = _libs['adyen_pos'].refund
    refund.argtypes = [POINTER(refund_request), CFUNCTYPE(UNCHECKED(None), POINTER(refund_response), POINTER(None)), POINTER(None)]
    refund.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/refund_extern.h: 41
if hasattr(_libs['adyen_pos'], 'refund_allocate'):
    refund_allocate = _libs['adyen_pos'].refund_allocate
    refund_allocate.argtypes = []
    refund_allocate.restype = POINTER(refund_request)

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 23
class struct_anon_74(Structure):
    pass

struct_anon_74.__slots__ = [
    'merchant_account',
    'user_id',
    'password',
    'app_id',
]
struct_anon_74._fields_ = [
    ('merchant_account', String),
    ('user_id', String),
    ('password', String),
    ('app_id', String),
]

register_app_request = struct_anon_74 # /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 23

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 29
class struct_payment_method(Structure):
    pass

struct_payment_method.__slots__ = [
    'aid',
    'name',
]
struct_payment_method._fields_ = [
    ('aid', String),
    ('name', String),
]

payment_method = struct_payment_method # /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 29

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 44
class struct_anon_75(Structure):
    pass

struct_anon_75.__slots__ = [
    'supported_currencies_size',
    'supported_currencies',
    'supported_payment_methods_size',
    'supported_payment_methods',
    'associated_merchants_size',
    'associated_merchants',
    'AppRegisteredForOfflineUsage',
    'parsed_result',
]
struct_anon_75._fields_ = [
    ('supported_currencies_size', c_int),
    ('supported_currencies', POINTER(POINTER(c_char))),
    ('supported_payment_methods_size', c_int),
    ('supported_payment_methods', POINTER(POINTER(payment_method))),
    ('associated_merchants_size', c_int),
    ('associated_merchants', POINTER(POINTER(c_char))),
    ('AppRegisteredForOfflineUsage', c_int),
    ('parsed_result', ADYEN_RESULT),
]

register_app_response = struct_anon_75 # /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 44

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 47
if hasattr(_libs['adyen_pos'], 'register_app'):
    register_app = _libs['adyen_pos'].register_app
    register_app.argtypes = [POINTER(register_app_request), CFUNCTYPE(UNCHECKED(None), POINTER(register_app_response), POINTER(None)), POINTER(None)]
    register_app.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 48
if hasattr(_libs['adyen_pos'], 'register_app_allocate'):
    register_app_allocate = _libs['adyen_pos'].register_app_allocate
    register_app_allocate.argtypes = []
    register_app_allocate.restype = POINTER(register_app_request)

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 29
class struct__dev_callbacks(Structure):
    pass

struct__dev_callbacks.__slots__ = [
    'device_state_update_CB',
    'status_tender_additional_data',
    'status_tender_print_receipt',
    'status_tender_check_signature',
    'status_tender_DCC',
    'status_tender_referral',
    'status_tender_progress',
    'status_tender_balance_acquired',
    'status_tender_final',
    'echo_str',
]
struct__dev_callbacks._fields_ = [
    ('device_state_update_CB', CFUNCTYPE(UNCHECKED(None), POINTER(None), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_additional_data', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_print_receipt', CFUNCTYPE(UNCHECKED(None), POINTER(receipts_strct), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_check_signature', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_DCC', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_referral', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_progress', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_balance_acquired', CFUNCTYPE(UNCHECKED(None), POINTER(response_header), POINTER(ped_device_info), POINTER(None))),
    ('status_tender_final', CFUNCTYPE(UNCHECKED(None), POINTER(final_strct), POINTER(ped_device_info), POINTER(None))),
    ('echo_str', POINTER(None)),
]

device_callbacks = struct__dev_callbacks # /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 29

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 44
class struct_anon_76(Structure):
    pass

struct_anon_76.__slots__ = [
    'ped_board_retry_count',
    'address',
    'callbacks',
    'posregister_configured_name',
    'store',
    'number_of_payment_device_options',
    'payment_device_options',
    'external_reference',
]
struct_anon_76._fields_ = [
    ('ped_board_retry_count', c_int),
    ('address', String),
    ('callbacks', device_callbacks),
    ('posregister_configured_name', String),
    ('store', String),
    ('number_of_payment_device_options', c_int),
    ('payment_device_options', POINTER(ADYPaymentDeviceOption)),
    ('external_reference', POINTER(None)),
]

register_device_request = struct_anon_76 # /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 44

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 54
class struct_anon_77(Structure):
    pass

struct_anon_77.__slots__ = [
    'internal_ped_object',
    'terminal_id',
    'ped_device_state',
    'parsed_result',
]
struct_anon_77._fields_ = [
    ('internal_ped_object', POINTER(None)),
    ('terminal_id', String),
    ('ped_device_state', POINTER(ped_device_info)),
    ('parsed_result', ADYEN_RESULT),
]

register_device_response = struct_anon_77 # /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 54

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 58
if hasattr(_libs['adyen_pos'], 'remove_all_devices'):
    remove_all_devices = _libs['adyen_pos'].remove_all_devices
    remove_all_devices.argtypes = []
    remove_all_devices.restype = None

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 59
if hasattr(_libs['adyen_pos'], 'remove_device'):
    remove_device = _libs['adyen_pos'].remove_device
    remove_device.argtypes = [POINTER(None)]
    remove_device.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 60
if hasattr(_libs['adyen_pos'], 'remove_device_by_teminal_id'):
    remove_device_by_teminal_id = _libs['adyen_pos'].remove_device_by_teminal_id
    remove_device_by_teminal_id.argtypes = [String]
    remove_device_by_teminal_id.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 61
if hasattr(_libs['adyen_pos'], 'remove_device_by_address'):
    remove_device_by_address = _libs['adyen_pos'].remove_device_by_address
    remove_device_by_address.argtypes = [String]
    remove_device_by_address.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 62
if hasattr(_libs['adyen_pos'], 'register_device'):
    register_device = _libs['adyen_pos'].register_device
    register_device.argtypes = [POINTER(register_device_request), CFUNCTYPE(UNCHECKED(None), POINTER(register_device_response), POINTER(None)), POINTER(None)]
    register_device.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 63
if hasattr(_libs['adyen_pos'], 'register_dev_allocate'):
    register_dev_allocate = _libs['adyen_pos'].register_dev_allocate
    register_dev_allocate.argtypes = []
    register_dev_allocate.restype = POINTER(register_device_request)

ADYscreenStatus = c_int # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 19

enum_anon_78 = c_int # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 19

ADYLibraryScreenUnknown = 0 # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 19

ADYLibraryScreenAccepted = (ADYLibraryScreenUnknown + 1) # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 19

ADYLibraryScreenFailed = (ADYLibraryScreenAccepted + 1) # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 19

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 33
class struct_anon_79(Structure):
    pass

struct_anon_79.__slots__ = [
    'ped',
    'merchant_account',
    'terminal_id',
    'screen_xslt_file',
    'format_xml_B64',
]
struct_anon_79._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('terminal_id', String),
    ('screen_xslt_file', String),
    ('format_xml_B64', String),
]

show_screen_request = struct_anon_79 # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 33

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 39
class struct_anon_80(Structure):
    pass

struct_anon_80.__slots__ = [
    'screen_id',
    'screen_status',
    'parsed_result',
]
struct_anon_80._fields_ = [
    ('screen_id', c_int),
    ('screen_status', ADYscreenStatus),
    ('parsed_result', ADYEN_RESULT),
]

show_screen_response = struct_anon_80 # /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 39

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 41
if hasattr(_libs['adyen_pos'], 'get_show_screen_result_str'):
    get_show_screen_result_str = _libs['adyen_pos'].get_show_screen_result_str
    get_show_screen_result_str.argtypes = [ADYscreenStatus]
    if sizeof(c_int) == sizeof(c_void_p):
        get_show_screen_result_str.restype = ReturnString
    else:
        get_show_screen_result_str.restype = String
        get_show_screen_result_str.errcheck = ReturnString

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 42
if hasattr(_libs['adyen_pos'], 'show_screen_allocate'):
    show_screen_allocate = _libs['adyen_pos'].show_screen_allocate
    show_screen_allocate.argtypes = []
    show_screen_allocate.restype = POINTER(show_screen_request)

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 43
if hasattr(_libs['adyen_pos'], 'show_screen'):
    show_screen = _libs['adyen_pos'].show_screen
    show_screen.argtypes = [POINTER(show_screen_request), CFUNCTYPE(UNCHECKED(None), POINTER(show_screen_response), POINTER(None)), POINTER(None)]
    show_screen.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/show_screen_extern.h: 44
if hasattr(_libs['adyen_pos'], 'show_screen_arg'):
    show_screen_arg = _libs['adyen_pos'].show_screen_arg
    show_screen_arg.argtypes = [String, String, String, String, CFUNCTYPE(UNCHECKED(None), POINTER(show_screen_response), POINTER(None)), POINTER(None)]
    show_screen_arg.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 27
class struct_anon_81(Structure):
    pass

struct_anon_81.__slots__ = [
    'ped',
    'merchant_account',
    'terminal_id',
    'tender_reference',
    'max_transaction',
]
struct_anon_81._fields_ = [
    ('ped', POINTER(None)),
    ('merchant_account', String),
    ('terminal_id', String),
    ('tender_reference', String),
    ('max_transaction', c_int),
]

tx_store_query_request = struct_anon_81 # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 27

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 29
class struct__receipt_set(Structure):
    pass

struct__receipt_set.__slots__ = [
    'merchant_receipt',
    'card_holder_receipt',
    'type',
    'next',
]
struct__receipt_set._fields_ = [
    ('merchant_receipt', receipt),
    ('card_holder_receipt', receipt),
    ('type', receipt_type),
    ('next', POINTER(struct__receipt_set)),
]

receipt_set = struct__receipt_set # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 34

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 36
class struct__tx_store_report(Structure):
    pass

struct__tx_store_report.__slots__ = [
    'tender_reference',
    'amount_currency',
    'amount_value',
    'timestamp',
    'state',
    'capture_pending',
    'merchant_reference',
    'psp_reference',
    'masked_pan',
    'pos_entry_mode',
    'receipts',
    'next',
]
struct__tx_store_report._fields_ = [
    ('tender_reference', String),
    ('amount_currency', String),
    ('amount_value', c_long),
    ('timestamp', String),
    ('state', ADYTenderState),
    ('capture_pending', c_int),
    ('merchant_reference', String),
    ('psp_reference', String),
    ('masked_pan', String),
    ('pos_entry_mode', String),
    ('receipts', POINTER(receipt_set)),
    ('next', POINTER(struct__tx_store_report)),
]

tx_store_report = struct__tx_store_report # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 52

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 57
class struct_anon_82(Structure):
    pass

struct_anon_82.__slots__ = [
    'report',
    'parsed_result',
]
struct_anon_82._fields_ = [
    ('report', POINTER(tx_store_report)),
    ('parsed_result', ADYEN_RESULT),
]

tx_store_query_response = struct_anon_82 # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 57

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 59
if hasattr(_libs['adyen_pos'], 'tx_store_query_allocate'):
    tx_store_query_allocate = _libs['adyen_pos'].tx_store_query_allocate
    tx_store_query_allocate.argtypes = []
    tx_store_query_allocate.restype = POINTER(tx_store_query_request)

# /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 60
if hasattr(_libs['adyen_pos'], 'tx_store_query'):
    tx_store_query = _libs['adyen_pos'].tx_store_query
    tx_store_query.argtypes = [POINTER(tx_store_query_request), CFUNCTYPE(UNCHECKED(None), POINTER(tx_store_query_response), POINTER(None)), POINTER(None)]
    tx_store_query.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 57
class struct_anon_83(Structure):
    pass

struct_anon_83.__slots__ = [
    'retry_counter',
    'flags',
    'transaction_type',
    'ped',
    'terminal_id',
    'merchant_account',
    'tender_reference',
    'new_state',
    'adjust_amount',
    'adjust_currency',
    'process',
    'attendant_action_result_code',
    'auth_code',
    'gift_card_type',
    'card_number',
    'expiry_month',
    'expiry_year',
    'card_mask',
    'card_mask_min',
    'card_mask_max',
    'recurring_contract_flags',
    'recurring_contract_detail_name',
    'shopper_reference',
    'shopper_email',
    'additional_data_obj',
]
struct_anon_83._fields_ = [
    ('retry_counter', c_int),
    ('flags', c_uint32),
    ('transaction_type', ADYTransactionType),
    ('ped', POINTER(None)),
    ('terminal_id', String),
    ('merchant_account', String),
    ('tender_reference', String),
    ('new_state', ADYUpdateTenderNewState),
    ('adjust_amount', c_long),
    ('adjust_currency', String),
    ('process', c_int),
    ('attendant_action_result_code', ADYAttendantAction),
    ('auth_code', String),
    ('gift_card_type', String),
    ('card_number', String),
    ('expiry_month', c_int),
    ('expiry_year', c_int),
    ('card_mask', String),
    ('card_mask_min', c_int),
    ('card_mask_max', c_int),
    ('recurring_contract_flags', c_uint32),
    ('recurring_contract_detail_name', String),
    ('shopper_reference', String),
    ('shopper_email', String),
    ('additional_data_obj', POINTER(additional_data_struct)),
]

update_tender_request = struct_anon_83 # /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 57

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 62
class struct_anon_84(Structure):
    pass

struct_anon_84.__slots__ = [
    'update_status',
    'result',
]
struct_anon_84._fields_ = [
    ('update_status', ADYUpdateTenderStatus),
    ('result', ADYEN_RESULT),
]

update_tender_response = struct_anon_84 # /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 62

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 64
if hasattr(_libs['adyen_pos'], 'update_tender'):
    update_tender = _libs['adyen_pos'].update_tender
    update_tender.argtypes = [POINTER(update_tender_request)]
    update_tender.restype = c_int

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 65
if hasattr(_libs['adyen_pos'], 'update_tender_allocate'):
    update_tender_allocate = _libs['adyen_pos'].update_tender_allocate
    update_tender_allocate.argtypes = []
    update_tender_allocate.restype = POINTER(update_tender_request)

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 68
if hasattr(_libs['adyen_pos'], 'confirm_additional_data'):
    confirm_additional_data = _libs['adyen_pos'].confirm_additional_data
    confirm_additional_data.argtypes = [String, String, String, c_long, String, String, String, String, POINTER(additional_data_struct), ADYTransactionType]
    confirm_additional_data.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 69
if hasattr(_libs['adyen_pos'], 'confirm_additional_data_cardOperation'):
    confirm_additional_data_cardOperation = _libs['adyen_pos'].confirm_additional_data_cardOperation
    confirm_additional_data_cardOperation.argtypes = [String, String, String, c_long, POINTER(additional_data_struct)]
    confirm_additional_data_cardOperation.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 71
if hasattr(_libs['adyen_pos'], 'cancel_transaction'):
    cancel_transaction = _libs['adyen_pos'].cancel_transaction
    cancel_transaction.argtypes = [String, String]
    cancel_transaction.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 72
if hasattr(_libs['adyen_pos'], 'cancel_cardOperation'):
    cancel_cardOperation = _libs['adyen_pos'].cancel_cardOperation
    cancel_cardOperation.argtypes = [String, String]
    cancel_cardOperation.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 74
if hasattr(_libs['adyen_pos'], 'confirm_print_receipt'):
    confirm_print_receipt = _libs['adyen_pos'].confirm_print_receipt
    confirm_print_receipt.argtypes = [String, String, ADYAttendantAction]
    confirm_print_receipt.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 76
if hasattr(_libs['adyen_pos'], 'confirm_referral'):
    confirm_referral = _libs['adyen_pos'].confirm_referral
    confirm_referral.argtypes = [String, String, String, ADYAttendantAction]
    confirm_referral.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 78
if hasattr(_libs['adyen_pos'], 'confirm_signature'):
    confirm_signature = _libs['adyen_pos'].confirm_signature
    confirm_signature.argtypes = [String, String, ADYAttendantAction]
    confirm_signature.restype = ADYLibraryResult

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 84
class struct__ped_device(Structure):
    pass

ped_device = struct__ped_device # /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 84

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 32
def NELT(a):
    return (sizeof(a) / sizeof((a [0])))

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 352
try:
    ADYRecurringContractDefault = 0
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 353
try:
    ADYRecurringContractOneClick = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 354
try:
    ADYRecurringContractRecurring = 2
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 355
try:
    ADYRecurringContractPayout = 4
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/adyen_enum.h: 357
try:
    ADYRecurringContractMax = ADYRecurringContractPayout
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 28
try:
    MINIMAL_API_VERSION = 14
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 29
try:
    MAXIMAL_API_VERSION = 19
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 31
try:
    VERSION_STRING = '1.13.8'
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 32
try:
    SVN_REVISION = ''
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 34
try:
    USER_AGENT = 'Adyen_POS_library/1.13.8'
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 36
try:
    PLATFORM_STRING = 'LINUX'
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 37
try:
    PLATFORM_BITS = '64'
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 38
try:
    PLATFORM_CPU = 'intel'
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 40
try:
    BUILD_LIB_OPENSSL = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 41
try:
    BUILD_LIB_CURL = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 42
try:
    BUILD_LIB_XML = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 43
try:
    BUILD_LIB_FCGI = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 44
try:
    BUILD_LIB_Z = 1
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 16
try:
    REGISTER_APP_RESPONSE_LOG_SIZE = 4096
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 20
try:
    FLAG_UPDATE_TENDER_TRIGGER_EVENT_ON_FAIL = 32768
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 21
try:
    FLAG_UPDATE_TENDER_AUTOREJECT_SIG_FAIL = 16384
except:
    pass

# /home/app/pywebdriver/adyen/linux/lib_include/update_tender_extern.h: 22
try:
    FLAG_UPDATE_TENDER_RETRY_ON_FAIL = 8192
except:
    pass

payment_method = struct_payment_method # /home/app/pywebdriver/adyen/linux/lib_include/register_app_extern.h: 29

_dev_callbacks = struct__dev_callbacks # /home/app/pywebdriver/adyen/linux/lib_include/register_device_extern.h: 29

_receipt_set = struct__receipt_set # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 29

_tx_store_report = struct__tx_store_report # /home/app/pywebdriver/adyen/linux/lib_include/tx_store_query_extern.h: 36

_ped_device = struct__ped_device # /home/app/pywebdriver/adyen/linux/lib_include/poslibc.h: 84

# No inserted files


