#cmake -DCMAKE_BUILD_TYPE=Debug ../<source>
#cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ../<source>
#cmake -DCMAKE_BUILD_TYPE=Release ../<source>

cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(graphpy)

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

set(LINK_FLAGS_COMMON "-fopenmp")
link_directories(${CMAKE_SOURCE_DIR})

set(graphpy_source_files
    kernel_pybind.cpp
)

add_subdirectory(pybind11)

pybind11_add_module(graphpy ${graphpy_source_files})
set_target_properties(graphpy PROPERTIES  COMPILE_FLAGS ${COMPILE_FLAGS_COMMON}
                      LINK_FLAGS ${LINK_FLAGS_COMMON})

set(gp_source_files
    kernel.cu
    kernel.h
    op.h
    Makefile
)
add_custom_target(libgp.so ALL
                COMMAND ${CMAKE_MAKE_PROGRAM}
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                COMMENT "Buidling libgp.so"
                DEPENDS ${gp_source_files} )

ADD_DEPENDENCIES(graphpy libgp.so)
target_link_libraries(graphpy PRIVATE gp)

