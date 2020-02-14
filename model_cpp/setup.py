try:
    from distutils.core import setup, Extension
except:
    raise RuntimeError("\n\nPython distutils not found!\n")

# Definition of extension modules
cppModel = Extension('cppModel',
                 sources = ['condensed.cpp', 'model.cpp'], extra_compile_args=['-std=gnu++11'])

# Compile Python module
setup (ext_modules = [cppModel],
       name = 'cppModel',
       description = 'cppModel Python module',
       version = '1.0')