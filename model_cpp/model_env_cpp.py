import numpy as np
try:
    import cppModel
except:
    strErr = "\n\n`cppModel` module not found, "
    raise RuntimeError(strErr)

if __name__ == '__main__':
    controller = cppModel.controller_constructor(50,50,50,1000)
    print(cppModel.observeGrid(controller))
    cppModel.delete_controller(controller)