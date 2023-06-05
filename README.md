# deep-codegen
A tool to generate code for customizing deep learning libraries. The input file is `kernel.dsl`, running `python main.py` with the input in this file will generate the following files:
* `gp_apis.py`
* `kernel.h`
* `generated_pybind.h`
* `generated_classes.py`
* `generated_tf.py`
* `generated_sparse.py`

The `kernel.dsl` file should contain one line for each function the user wishes to generate. These lines should be formatted as C/C++ function declarations and should end with a semicolon. The return type should be `void`, and the first argument should be `graph`, of the type `graph_t&`. The last two arguments should be `op`, of the type `op_t`, and `reverse`, of the type `int64_t`. After `graph`, the input arguments should be added. There can be multiple inputs. Each should contain the string `input` somewhere in the name of the argument. Each input should be of the type `array{$x}d_t<float>&`, where `{$x}` is the dimension of the input. After the inputs, the outputs should be added. The output should be called `output` if there is only one, and they should be named `output1`, `output2`, `output3`, etc. if there is more than one output. If there are multiple outputs, the python functions will return multiple values, one for each output.