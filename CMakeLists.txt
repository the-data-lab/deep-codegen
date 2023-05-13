#cmake -DCMAKE_BUILD_TYPE=Debug ../<source>
#cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ../<source>
#cmake -DCMAKE_BUILD_TYPE=Release ../<source>

cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(Kernel)

set(CMAKE_CXX_STANDARD 14)  # enable C++11 standard
set(CMAKE_CXX_STANDARD_REQUIRED ON)
#set(CMAKE_CXX_EXTENSIONS ON)


# Set a default build type if none was specified
set(default_build_type "Release")
   
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
   message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
   set_property(CACHE CMAKE_BUILD_TYPE PROPERTY VALUE "${default_build_type}")
endif()

set(COMPILE_FLAGS_COMMON "-Wno-unused-result -D_FILE_OFFSET_BITS=64 -fPIC -march=native -mfpmath=sse -msse4.2 -mavx2 -ffast-math -fopenmp")

set(COMPILE_FLAGS_GONE32 "${COMPILE_FLAGS_COMMON} -DB32")
set(COMPILE_FLAGS_GONE64 "${COMPILE_FLAGS_COMMON} -DB64")

set(LINK_FLAGS_COMMON "-fopenmp")
link_directories(${CMAKE_SOURCE_DIR})

set(kernel_source_files
    kernel_pybind.cpp
)


add_subdirectory(pybind11)

pybind11_add_module(kernel ${kernel_source_files})
set_target_properties(kernel PROPERTIES  COMPILE_FLAGS ${COMPILE_FLAGS_GONE32}
                      LINK_FLAGS ${LINK_FLAGS_COMMON})

#set(spmm_source_files
#    spmmv_coo.cu
#    spmme_coo.cu
#    spmmve_coo.cu
#    spmm.cu
#    kernel.cu
#    spmmve.cu
#    sddmme.cu
#    kernel_coo.cu
#    kernel.h
#    op.h
#    Makefile
#)
#add_custom_target(libspmm.so ALL
#                COMMAND ${CMAKE_MAKE_PROGRAM}
#                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
#                COMMENT "Buidling libspmm.so"
#                DEPENDS ${spmm_source_files} )
#
#ADD_DEPENDENCIES(kernel libspmm.so)
#target_link_libraries(kernel PRIVATE spmm)

