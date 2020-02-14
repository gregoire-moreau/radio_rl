try:
    from distutils.core import setup, Extension
except:
    raise RuntimeError("\n\nPython distutils not found!\n")

# Definition of extension modules
cppModel = Extension('cppModel',
                 sources = ['cell.cpp', 'grid.cpp', 'controller.cpp', 'model.cpp'])

# Compile Python module
setup (ext_modules = [cppModel],
       name = 'cppModel',
       description = 'cppModel Python module',
       version = '1.0')