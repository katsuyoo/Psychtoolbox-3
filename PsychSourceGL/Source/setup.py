# setup.py -- Build-Script for building Psychtoolbox-3 "mex" files as Python extensions.
#
# (c) 2018 Mario Kleiner - All rights reserved.
#

from distutils.core import setup, Extension # Build system.
import os, fnmatch                          # Directory traversal, file list building.
import platform                             # OS detection.

def get_sourcefiles(path):
    sources = [];
    pattern = '*.c';
    for filename in os.listdir(path):
        if fnmatch.fnmatch(filename, pattern):
            sources += [os.path.join(path,filename)];

    # Fancy schmanzi, not needed atm. for recursive dir traversal:
    #    for root, dirs, files in os.walk(path):
    #        for filename in files:
    #            sources += [os.path.join(root,filename)];

    return(sources);


# No "no reproducible builds" warning:
base_compile_args = ['-Wno-date-time'];

# Treating some special cases like Octave seems to be the right thing to do,
# PSYCH_LANGUAGE setting is self-explanatory:
base_macros = [('PTBOCTAVE3MEX', None), ('PSYCH_LANGUAGE', 'PSYCH_PYTHON')];

# All libraries to link to all modules:
base_libs = ['c', 'rt'];

# Common infrastructure and the scripting glue module for interfacing with the Python runtime:
basefiles_common = get_sourcefiles('./Common/Base') + ['Common/Base/PythonGlue/PsychScriptingGluePython.c'];
baseincludes_common = ['Common/Base', 'Common/Screen'];

# Linux specific backend code:
basefiles_linux = get_sourcefiles('./Linux/Base/');
baseincludes_linux = ['Linux/Base'];

# OS detection and file selection for the different OS specific backends:
print 'Platform reported as: ' + platform.system();
if platform.system() == 'Linux':
    print 'Building for Linux...\n';
    osname = 'Linux';
    basefiles_os = basefiles_linux;
    baseincludes_os = baseincludes_linux;

if platform.system() == 'Windows':
    print 'Building for Windows...\n';
    osname = 'Windows';
    basefiles_os = basefiles_windows;
    baseincludes_os = baseincludes_windows;

if platform.system() == 'Darwin':
    print 'Building for macOS...\n';
    osname = 'OSX';
    basefiles_os = basefiles_osx;
    baseincludes_os = baseincludes_osx;

# GetSecs module: Clock queries.
name = 'GetSecs';
GetSecs = Extension(name,
                    extra_compile_args = base_compile_args,
                    define_macros = [('PTBMODULE_' + name, None)] + base_macros,
                    include_dirs = ['Common/' + name] + baseincludes_common + baseincludes_os,
                    sources = basefiles_common + basefiles_os + get_sourcefiles('./Common/' + name),
                    libraries = base_libs
                   )

# WaitSecs module: Timed waits.
name = 'WaitSecs';
WaitSecs = Extension(name,
                     extra_compile_args = base_compile_args,
                     define_macros = [('PTBMODULE_' + name, None)] + base_macros,
                     include_dirs = ['Common/' + name] + baseincludes_common + baseincludes_os,
                     sources = basefiles_common + basefiles_os + get_sourcefiles('./Common/' + name),
                     libraries = base_libs
                    )

# PsychPortAudio module: High precision, high reliability, multi-channel, multi-card audio i/o.
name = 'PsychPortAudio';
PsychPortAudio = Extension(name,
                           extra_compile_args = base_compile_args,
                           define_macros = [('PTBMODULE_' + name, None)] + base_macros,
                           include_dirs = ['Common/' + name] + baseincludes_common + baseincludes_os,
                           sources = basefiles_common + basefiles_os + get_sourcefiles('./Common/' + name),
                           libraries = base_libs + ['asound'],
                           extra_objects = ['/usr/local/lib/libportaudio.a']
                          )

# PsychHID module: Note all the unusual include_dirs, and other special includes,
#                  sources, libs etc.
name = 'PsychHID';
PsychHID = Extension(name,
                     extra_compile_args = base_compile_args,
                     define_macros = [('PTBMODULE_' + name, None)] + base_macros,
                     include_dirs = ['Common/' + name] + baseincludes_common + baseincludes_os + ['Linux/' + name] + ['/usr/include/libusb-1.0'],
                     sources = basefiles_common + basefiles_os + get_sourcefiles('./Common/' + name) + get_sourcefiles('./' + osname + '/' + name),
                     libraries = base_libs + ['dl', 'usb-1.0', 'X11', 'Xi', 'util']
                    )

setup (name = 'Psychtoolbox4Python',
        version = '0.1',
        description = 'This is the prototype of a port of Psychtoolbox-3 mex files to Python extensions.',
        ext_modules = [GetSecs, WaitSecs, PsychPortAudio, PsychHID]
      )
