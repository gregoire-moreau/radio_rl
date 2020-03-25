try:
    from distutils.core import setup, Extension
    import numpy
except:
    raise RuntimeError("\n\nPython distutils not found!\n")

# Definition of extension modules
cppCellModel = Extension('cppCellModel',
                 sources = ['cell.cpp', 'grid.cpp', 'controller.cpp', 'model.cpp'], extra_compile_args=['-std=gnu++11'],
                include_dirs = [numpy.get_include()])

# Compile Python module
setup (ext_modules = [cppCellModel],
       name = 'cppCellModel',
       description = 'cppModel Python module',
       version = '1.0')