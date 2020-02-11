//http://www.speedupcode.com/c-class-in-python3/
//https://www.tutorialspoint.com/python/python_further_extensions.htm
//https://scipy-lectures.org/advanced/interfacing_with_c/interfacing_with_c.html#id1

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include "controller.h"
#include <numpy/npy_common.h>
#include <numpy/arrayobject.h>
#include <iostream>



PyObject* controller_constructor(PyObject* self, PyObject* args){
    // Arguments passed from Python
    int xsize;
    int ysize;
    int source_nums;
    int init_steps;

    // Process arguments passes from Python
    PyArg_ParseTuple(args, "iiii",
                     &xsize,
                     &ysize,
                     &source_nums,
                     &init_steps);

    Controller * controller = new Controller(1000, xsize, ysize, source_nums);

    PyObject* controllerCapsule = PyCapsule_New((void *)controller, "ControllerPtr", NULL);
    PyCapsule_SetPointer(controllerCapsule, (void *)controller);

    for (int i = 0; i < init_steps; i++)
        controller -> go();

    return Py_BuildValue("O", controllerCapsule);
}


PyObject* go(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    int num_steps;

    PyArg_ParseTuple(args, "Oi",
                     &controllerCapsule,
                     &num_steps);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    for (int i = 0; i < num_steps; i++)
        controller -> go();
    //std::cout << "Tick : " << controller->tick << " HCells : " << HealthyCell::count << " CCells : " << CancerCell::count << std::endl;
    
    Py_RETURN_NONE;
}


PyObject* irradiate(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double dose;

    PyArg_ParseTuple(args, "Od",
                     &controllerCapsule,
                     &dose);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    controller -> irradiate(dose);
    
    Py_RETURN_NONE;
}


PyObject* delete_controller(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    delete controller;

    Py_RETURN_NONE;
}

PyObject *HCellCount(PyObject *self) {
   return Py_BuildValue("i", HealthyCell::count);
}

PyObject *CCellCount(PyObject *self) {
   return Py_BuildValue("i", CancerCell::count);
}

PyObject* observeGrid(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    int ** out_dataptr;
    NpyIter *out_iter;
    int x = 0;
    NpyIter_IterNextFunc *out_iternext;
    PyObject* out_array;

    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    npy_intp dims[2] = {controller->xsize, controller->ysize};
    out_array = PyArray_SimpleNew(2, dims, NPY_INT);
    if (out_array == NULL)
        return NULL;
    
    out_iter = NpyIter_New((PyArrayObject *)out_array, NPY_ITER_READWRITE,
                          NPY_KEEPORDER, NPY_NO_CASTING, NULL);
    if (out_iter == NULL) {
        NpyIter_Deallocate(out_iter);
        goto fail;
    }
    out_iternext = NpyIter_GetIterNext(out_iter, NULL);
    if (out_iternext == NULL) {
        NpyIter_Deallocate(out_iter);
        goto fail;
    }
    out_dataptr = (int **) NpyIter_GetDataPtrArray(out_iter);
    do {
        **out_dataptr = controller->cell_types(x / controller->ysize, x % controller->ysize);
        x++;
    } while(out_iternext(out_iter));

    Py_INCREF(out_array);
    NpyIter_Deallocate(out_iter);
    return out_array;

    fail:
        Py_XDECREF(out_array);
        return NULL;
}



PyMethodDef cppModelFunctions[] =
{

    {"controller_constructor", 
      controller_constructor, METH_VARARGS,
     "Create Controller"},

    {"go",
      go, METH_VARARGS,
     "Simulate a number of steps"},

    {"irradiate",
      irradiate, METH_VARARGS,
     "Irradiate the tumor with a certain dose"},

    {"delete_controller",
      delete_controller, METH_VARARGS,
     "Delete Controller"},

    {"HCellCount",
      (PyCFunction)HCellCount, METH_NOARGS,
     "Number of healthy cells"},
    
    {"CCellCount",
      (PyCFunction)CCellCount, METH_NOARGS,
     "Number of cancer cells"},

    {"observeGrid",
      observeGrid, METH_VARARGS,
     "Observation of cell types"},

    {NULL, NULL, 0, NULL} 
};


struct PyModuleDef cppModelModule =
{
   PyModuleDef_HEAD_INIT,
   "cppModel",
   NULL,
   -1,
   cppModelFunctions
};

PyMODINIT_FUNC PyInit_cppModel(void)
{
    import_array();
    return PyModule_Create(&cppModelModule);
}