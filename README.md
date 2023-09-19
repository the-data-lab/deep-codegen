# deep-codegen
A tool to generate code for customizing deep learning libraries. This tool converts `deep learning library development` to `independent code` development by removing all the dependencies that a deep learning framework, such as Pytorch or Tensorflow brings. As you are aware, writing independent code for education and research is faster than modifying an existing framework.

The input file is `kernel.dsl`, running `python main.py` with the input in this file will generate the following files to add productivity to deep learning system library development, and their integration with deep learning framework(s):

The generated back-end code (independent of Pytorch or Tensorflow):
* `kernel.h`
* `kernel.cu` with a dummy implementation
* `generated_pybind.h`


For the front-end code for PyTorch, we generate the following files (thoroughly evaluated):
* `gp_apis.py`
* `pytorch_apis.py`

For the front-end code for TensorFlow, we generate the following files (less tested): 
* `gp_apis_tf.py`
* `tf_apis.py`


The `kernel.dsl` file should contain one line for each kernel API the user wishes to implement. These lines should be formatted as C/C++ function declarations and end with a semicolon. The return type should be `void`. 
There can be multiple input tensors in a kernel. Each input tensor should be of the type `array{$x}d_t<float>&`, where `{$x}` is the dimension of the input. After the input tensor arguments, the output tensor arguments should be added, which also relies on `array{$x}d_t<float>&` class type. The output should be called `output` if there is only one, and they should be named `output1`, `output2`, `output3`, etc. if there is more than one output. If there are multiple outputs, the Python APIs will return multiple values, one for each output.

The generator supports any custom class, such as a blind class `graph_t`, and can be used in the kernel API specification. Other built in data-types are supported as well.

# Cloning, Compilation, and testing
After cloning (git clone ...), please run this command.
`git submodule update --init --recursive` This brings pybind11 code to your cloned locations. See `https://git-scm.com/book/en/v2/Git-Tools-Submodules` for more information on how to work with sub-modules

For code generation, run the following commands after kernel.dsl has been populated with the APIs that you are planning to implement yourself:
```
python main.py
```

For compilation, run the following command
```
mkdir build
cd build
cmake ../
make
```

This will produce a binary, something like `graphpy.cpython-38-x86_64-linux-gnu.so`. This file is the back-end library that contains Python binding and Cuda kernels. If you paste it into the deep-codegen directory, you can import the useful functionalities by using the following commands, where we have imported pytorch_apis.py:
```
pkumar@mira0:~/src/deep-codegen/build$ pwd
/home/pkumar/src/deep-codegen/build
pkumar@mira0:~/src/deep-codegen/build$ cp graphpy.cpython-38-x86_64-linux-gnu.so ../
pkumar@mira0:~/src/deep-codegen/build$ cd ../
pkumar@mira0:~/src/deep-codegen$ python3 
Python 3.8.10 (default, May 26 2023, 14:05:08) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pytorch_apis
>>> 
```

For calling the actual APIs that you have implemented as part of the class assignment, we will be testing the same APIs but now using PyTorch and Python.
You can call any of the APIs that you generated, or you can call PyTorch APIs, there is no difference.
