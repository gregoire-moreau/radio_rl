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

PyObject* controller_constructor_oar(PyObject* self, PyObject* args){
    // Arguments passed from Python
    int xsize;
    int ysize;
    int source_nums;
    int init_steps;
    int x1, x2, y1, y2;

    // Process arguments passes from Python
    PyArg_ParseTuple(args, "iiiiiiii",
                     &xsize,
                     &ysize,
                     &source_nums,
                     &init_steps,
                     &x1,
                     &x2,
                     &y1,
                     &y2);

    Controller * controller = new Controller(1000, xsize, ysize, source_nums, x1, x2, y1, y2);

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

PyObject* irradiate_radius(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double dose;
    double radius;
    PyArg_ParseTuple(args, "Odd",
                     &controllerCapsule,
                     &dose,
                     &radius);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    controller -> irradiate(dose, radius);

    Py_RETURN_NONE;
}

PyObject* irradiate_center_radius(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double dose;
    double radius;
    PyArg_ParseTuple(args, "Odd",
                     &controllerCapsule,
                     &dose,
                     &radius);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    controller -> irradiate_center(dose, radius);

    Py_RETURN_NONE;
}

PyObject* irradiate_center(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double dose;
    PyArg_ParseTuple(args, "Od",
                     &controllerCapsule,
                     &dose);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    controller -> irradiate_center(dose);

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

PyObject *OARCellCount(PyObject *self) {
   return Py_BuildValue("i", OARCell::count);
}

PyObject* controllerTick(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    return Py_BuildValue("i", controller -> tick);
}

PyObject* tumor_radius(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    return Py_BuildValue("f", controller -> tumor_radius());
}

PyObject* get_center_x(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    return Py_BuildValue("f", controller -> get_center_x());
}

PyObject* get_center_y(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");

    return Py_BuildValue("f", controller -> get_center_y());
}

PyObject* observeDensity(PyObject* self, PyObject* args){
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
        **out_dataptr = controller->pixel_density(x / controller->ysize, x % controller->ysize);
        x++;
    } while(out_iternext(out_iter));

    Py_INCREF(out_array);
    NpyIter_Deallocate(out_iter);
    return out_array;

    fail:
        Py_XDECREF(out_array);
        return NULL;
}

PyObject* observeSegmentation(PyObject* self, PyObject* args){
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
        **out_dataptr = controller->pixel_type(x / controller->ysize, x % controller->ysize);
        x++;
    } while(out_iternext(out_iter));

    Py_INCREF(out_array);
    NpyIter_Deallocate(out_iter);
    return out_array;

    fail:
        Py_XDECREF(out_array);
        return NULL;
}


PyObject* observeGlucose(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double ** out_dataptr;
    NpyIter *out_iter;
    int x = 0;
    NpyIter_IterNextFunc *out_iternext;
    PyObject* out_array;
    double ** glucose;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    
    glucose = controller->currentGlucose();
    
    npy_intp dims[2] = {controller->xsize, controller->ysize};
    out_array = PyArray_SimpleNew(2, dims, NPY_DOUBLE);
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
    out_dataptr = (double **) NpyIter_GetDataPtrArray(out_iter);
    do {
        **out_dataptr = glucose[x / controller -> ysize][x % controller -> ysize];
        x++;
    } while(out_iternext(out_iter));

    Py_INCREF(out_array);
    NpyIter_Deallocate(out_iter);
    return out_array;

    fail:
        Py_XDECREF(out_array);
        return NULL;
}

PyObject* observeOxygen(PyObject* self, PyObject* args){
    PyObject* controllerCapsule;
    double ** out_dataptr;
    NpyIter *out_iter;
    int x = 0;
    NpyIter_IterNextFunc *out_iternext;
    PyObject* out_array;
    double ** oxygen;
    PyArg_ParseTuple(args, "O",
                     &controllerCapsule);

    Controller* controller = (Controller*)PyCapsule_GetPointer(controllerCapsule, "ControllerPtr");
    
    oxygen = controller->currentOxygen();
    
    npy_intp dims[2] = {controller->xsize, controller->ysize};
    out_array = PyArray_SimpleNew(2, dims, NPY_DOUBLE);
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
    out_dataptr = (double **) NpyIter_GetDataPtrArray(out_iter);
    do {
        **out_dataptr = oxygen[x / controller -> ysize][x % controller -> ysize];
        x++;
    } while(out_iternext(out_iter));

    Py_INCREF(out_array);
    NpyIter_Deallocate(out_iter);
    return out_array;

    fail:
        Py_XDECREF(out_array);
        return NULL;
}



PyMethodDef cppCellModelFunctions[] =
{

    {"controller_constructor", 
      controller_constructor, METH_VARARGS,
     "Create Controller"},

    {"controller_constructor_oar", 
      controller_constructor_oar, METH_VARARGS,
     "Create Controller with oar zone"},

    {"go",
      go, METH_VARARGS,
     "Simulate a number of steps"},

    {"irradiate",
      irradiate, METH_VARARGS,
     "Irradiate the tumor with a certain dose"},

     {"irradiate_radius",
      irradiate_radius, METH_VARARGS,
     "Irradiate the tumor with a certain dose and a certain radius"},

     {"irradiate_center",
      irradiate_center, METH_VARARGS,
     "Irradiate the tumor with a certain dose at the center of the grid"},

     {"irradiate_center_radius",
      irradiate_center, METH_VARARGS,
     "Irradiate the tumor with a certain dose at the center of the grid with a certain radius"},

    {"delete_controller",
      delete_controller, METH_VARARGS,
     "Delete Controller"},

    {"HCellCount",
      (PyCFunction)HCellCount, METH_NOARGS,
     "Number of healthy cells"},
    
    {"CCellCount",
      (PyCFunction)CCellCount, METH_NOARGS,
     "Number of cancer cells"},

    {"OARCellCount",
      (PyCFunction)OARCellCount, METH_NOARGS,
     "Number of cancer cells"},

    {"observeDensity",
      observeDensity, METH_VARARGS,
     "Observation of cell type densities"},
    
    {"observeGlucose",
      observeGlucose, METH_VARARGS,
     "Observation of glucose"},

     {"observeOxygen",
      observeOxygen, METH_VARARGS,
     "Observation of oxygen"},

     {"observeSegmentation",
      observeSegmentation, METH_VARARGS,
     "Observation of pixel types"},
     {"tumor_radius",
      tumor_radius, METH_VARARGS,
     "Observation of oxygen"},
     {"get_center_x",
      get_center_x, METH_VARARGS,
     "X coordinate of tumour's center"},
     {"get_center_y",
      get_center_y, METH_VARARGS,
     "Y coordinate of tumour's center"},
     {"controllerTick",
      controllerTick, METH_VARARGS,
     "Number of ticks for current controller"},

    {NULL, NULL, 0, NULL} 
};


struct PyModuleDef cppCellModelModule =
{
   PyModuleDef_HEAD_INIT,
   "cppCellModel",
   NULL,
   -1,
   cppCellModelFunctions
};

PyMODINIT_FUNC PyInit_cppCellModel(void)
{
    import_array();
    return PyModule_Create(&cppCellModelModule);
}
