#include <pybind11/pybind11.h>
#include<pybind11/numpy.h>
#include <iostream>


#include "dlpack.h"
#include "kernel.h"
#include "csr.h"

using std::cout;
using std::endl;
namespace py = pybind11;

array1d_t<float> capsule_to_array1d(py::capsule& capsule) 
{
    //DLManagedTensor * dlMTensor = (DLManagedTensor *)PyCapsule_GetPointer(&input, "dltesnor");
    //The worst static_cast, this is becacuse of 'operator T*()' in pybind11 code
    //Pybind11 should have simply provided GetPointer() API.

    DLManagedTensor * dlMTensor = static_cast<DLManagedTensor*>(capsule);
    assert(dlMTensor);
    DLTensor* tensor = &dlMTensor->dl_tensor;
    
    int shape0 = tensor->shape[0];
    float*  data_ptr = (float*)tensor->data;

    array1d_t<float> array(data_ptr, shape0);
    return array;
}

array2d_t<float> capsule_to_array2d(py::capsule& capsule) 
{
    DLManagedTensor * dlMTensor = static_cast<DLManagedTensor*>(capsule);
    assert(dlMTensor);
    DLTensor* tensor = &dlMTensor->dl_tensor;
    
    int shape0 = tensor->shape[0];
    int shape1 = tensor->shape[1];
    float*  data_ptr = (float*)tensor->data;

    array2d_t<float> array(data_ptr, shape0, shape1);
    return array;
}

array3d_t<float> capsule_to_array3d(py::capsule& capsule) 
{
    DLManagedTensor * dlMTensor = static_cast<DLManagedTensor*>(capsule);
    assert(dlMTensor);
    DLTensor* tensor = &dlMTensor->dl_tensor;
    
    int shape0 = tensor->shape[0];
    int shape1 = tensor->shape[1];
    int shape2 = tensor->shape[2];
    float*  data_ptr = (float*)tensor->data;

    array3d_t<float> array(data_ptr, shape0, shape1, shape2);
    return array;
}

array4d_t<float> capsule_to_array4d(py::capsule& capsule) 
{
    DLManagedTensor * dlMTensor = static_cast<DLManagedTensor*>(capsule);
    assert(dlMTensor);
    DLTensor* tensor = &dlMTensor->dl_tensor;
    
    int shape0 = tensor->shape[0];
    int shape1 = tensor->shape[1];
    int shape2 = tensor->shape[2];
    int shape3 = tensor->shape[3];
    float*  data_ptr = (float*)tensor->data;

    array4d_t<float> array(data_ptr, shape0, shape1, shape2, shape3);
    return array;
}

#include "generated_pybind.h"

PYBIND11_MODULE(graphpy, m) {
    
  py::enum_<op_t>(m, "op_t", py::arithmetic(), "Operations Enums")
        .value("eSUM", eSUM, "sum")
        .value("eMAX", eMAX, "max")
        .value("eMIN", eMIN, "min")
        .value("eSUB", eSUB, "sub")
        .value("eMUL", eMUL, "mul")
        .value("eDIV", eDIV, "div")
        .export_values();

  py::class_<graph_t>(m, "graph_t")
    .def(py::init<>())
    .def("save_graph", &graph_t::save_graph)
    .def("get_vcount", &graph_t::get_vcount)
    .def("get_edge_count", &graph_t::get_ecount)

    ;
    
    
  m.def("init_graph",
      [](py::array offset_csr, py::array nebrs_csr, py::array offset_csc, py::array nebrs_csc, int flag, int num_vcount) {
           graph_t* graph =  new graph_t;
           //cout<< offset_csr.shape(0) - 1<< "num_vcount"<< endl;
           graph->init(offset_csr.shape(0) - 1, nebrs_csr.itemsize(), 
                 offset_csr.request().ptr, nebrs_csr.request().ptr,
                 offset_csc.request().ptr, nebrs_csc.request().ptr, flag, num_vcount);
            //THD_COUNT = thd_count;
           return graph;
      }
  );

  m.def("load_graph",
      [](const string& odir) {
            graph_t* graph = new graph_t;
            graph->load_graph(odir);
            return graph;
      }
  );
  m.def("load_graph_noeid",
      [](const string& odir) {
            graph_t* graph = new graph_t;
            graph->load_graph_noeid(odir);
            return graph;
      }
  );
  
  export_kernel(m);
}


