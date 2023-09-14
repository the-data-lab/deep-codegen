#pragma once

#include <string>
#include <cstring>
#include <cassert>
#include "op1.h"

#define FULL_WARP_MASK 0xFFFFFFFF
#define WARP_SIZE  32
#define WARP_BIT  5

#define BLOCK_SIZE 128
#define BLOCK_BIT 7

#define WARP_PER_BLOCK 4
#define WARP_PER_BLOCK_BIT 2
            
#define BLOCK_EDGE_BIT 8
#define WARP_EDGE_BIT 6

#define EDGE_CHUNK 4
#define WARP_EDGE_CHUNK (WARP_SIZE*EDGE_CHUNK)
#define BLOCK_EDGE_CHUNK (BLOCK_SIZE*EDGE_CHUNK)

#define CHUNK 4
#define WARP_CHUNK (WARP_SIZE*CHUNK)
#define BLOCK_CHUNK (BLOCK_SIZE*CHUNK)


#ifdef __CUDACC__
#define CUDA_CALLABLE_MEMBER __host__ __device__
#define CUDA_ONLY  __device__
#else
#define CUDA_CALLABLE_MEMBER
#define CUDA_ONLY
#endif

#define MAX_VID 0xFFFFFFFF


typedef float (*op_scalar_fn)(float, float);


template <class T>
CUDA_ONLY T warp_reduce(T val){
    for(int offset = 16; offset > 0; offset /= 2)
        val+= __shfl_down_sync (FULL_WARP_MASK,val,offset);
    return val;
}

template <class T>
CUDA_ONLY T warp_reduce_op(T val, op_scalar_fn op_fn){
    for(int offset = 16; offset > 0; offset /= 2)
        val = op_fn(val, __shfl_down_sync (FULL_WARP_MASK,val,offset));
    return val;
}


CUDA_ONLY inline float add_scalar(float x, float y) {
    return x + y;
}

CUDA_ONLY inline float sub_scalar(float x, float y) {
    return x - y;
}

CUDA_ONLY inline float max_scalar(float x, float y) {
    if(x>y) return x;
    else return y;
}

CUDA_ONLY inline float min_scalar(float x, float y) {
    if(x<y) return x;
    else return y;
}

CUDA_ONLY inline float mul_scalar(float x, float y) {
    return x * y;
}

CUDA_ONLY inline float div_scalar(float x, float y) {
    return x / y;
}


//if the kernel itself need the fuction pointer
CUDA_ONLY inline op_scalar_fn get_fn_kernel(op_t op) {
    op_scalar_fn op_fn;
    
    if (op == eDIV) {
        op_fn = div_scalar;
    } else if (op == eSUB) {
        op_fn = sub_scalar;
    } else if (op == eSUM) {
        op_fn = add_scalar;
    } else if (op == eMUL) {
        op_fn = mul_scalar;
    } else if (op == eMIN) {
        op_fn = min_scalar;
    } else if (op == eMAX) {
        op_fn = max_scalar;
    } else {
        assert(0);
    }
    return op_fn;
}

template <class T>
struct array1d_t {
    T* data_ptr;
    int col_count;
    array1d_t(T* ptr, int col) 
            : data_ptr(ptr), col_count(col) { }
};



//2D tensor
template <class T>
struct array2d_t {
    T* data_ptr;
    int row_count;
    int col_count;
    array2d_t(T* ptr, int row,  int col) 
            : data_ptr(ptr), row_count (row),col_count(col) { }

};

//3D tensor
template <class T>
struct array3d_t {
    T* data_ptr;
    int matrix_count;
    int row_count;
    int col_count;
    array3d_t(T* ptr, int matrix, int row, int col) 
            : data_ptr(ptr), matrix_count (matrix), row_count (row),col_count(col) { }
};


//4D tensor
template <class T>
struct array4d_t {
    T* data_ptr;
    int last_count;
    int matrix_count;
    int row_count;
    int col_count;
    array4d_t(T* ptr, int last, int matrix, int row, int col) 
            : data_ptr(ptr), last_count(last), matrix_count (matrix), row_count (row),col_count(col) { }
};
