import sysconfig
try:
    from distutils.core import setup, Extension
except:
    raise RuntimeError("\n\nPython distutils not found!\n")

extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
extra_compile_args += ["-std=c++11", '-Wall', "-Wextra"]

# Definition of extension modules
cppModel = Extension('cppModel',
                 sources = ['cell.cpp', 'grid.cpp', 'controller.cpp', 'model.cpp'], extra_compile_args = extra_compile_args, language='c++11')

# Compile Python module
setup (ext_modules = [cppModel],
       name = 'cppModel',
       description = 'cppModel Python module',
       version = '1.0')
