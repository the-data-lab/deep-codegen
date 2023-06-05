INDENTATION = '    '

#get function name
def get_fuc_name(fuc_var):
    result = fuc_var[0].split(" ")
    return result[-1]

#remove empty strings from a list of strings
def remove_empty_string(string_list):
    return [item for item in string_list if item != '']

#remove unnecessary characters (newline and closing parenthesis) from string
def remove_unnecessary_chars(string):
    for unnecessary_char in ['\n', ')']:
        if unnecessary_char in string:
            string = string.replace(unnecessary_char, '')
    return string

def cal_array_class(array_dim_list, i):
    each_element = array_dim_list[i]
    for i in range(3):
        if str(i+1) in each_element[0]:
            return str(i+1)
    return "10000"

# record the num of class
def record_num_class(var_list, array_index_list, array_dim_list):
    class_choice = ["graph", "array", "op", "reverse"]
    output_list = []
    for (i, var_list_item) in enumerate(var_list):
        if i in array_index_list:
            temp1 = [1, var_list_item]
            array_class = cal_array_class(array_dim_list, i)
            temp1.append(int(array_class))
            output_list.append(temp1)
        else:
            class_dict = {'graph': 0, 'op': 2, 'reverse': 3, 'norm': 4}
            for class_key in class_dict:
                if class_key in var_list_item:
                    output_list.append([class_dict[class_key], class_key])
                    break
    return output_list

#get a list of arguments for the function
def get_arguments(var_list, array_dim_list, output_index_list, array_index_list):
    class_choice = ["graph", "array", "op", "reverse"]
    output_list = []
    for (i, var_list_item) in enumerate(var_list):
        if i in array_index_list:
            temp1 = [1, var_list_item]
            array_class = cal_array_class(array_dim_list, i)
            temp1.append(int(array_class))
            output_list.append(temp1)
        elif i in output_index_list:
            temp1 = [4, var_list_item]
            array_class = cal_array_class(array_dim_list, i)
            temp1.append(int(array_class))
            output_list.append(temp1)
        else:
            number_dict = {"graph": 0, "op": 2, "reverse": 3, "norm": 5}
            for key in number_dict:
                if key in var_list_item:
                    output_list.append([number_dict[key], key])
                    break
    return output_list

#get the arguments in a string
def make_arguments(output_list, string_dict):
    num_of_dlpack_index = []
    num_of_dlpack_name = []
    write_string = ""
    for (j, item) in enumerate(output_list):
        if item[0] in string_dict:
            write_string += f'{string_dict[item[0]]}, '
        elif item[0] == 1:
            num_of_dlpack_index.append(j)
            num_of_dlpack_name.append(item[1])
            write_string += f'{item[1]}, '
        elif (item[0] == 4) and (item[2] in range(1, 4)):
            id = item[1].replace("output", "")
            write_string += ', '.join(f'dim{id}_{i}' for i in range(item[2])) + ', '
    write_string += "device0" #remove final comma/space and add ender
    return write_string

def fuc_var_class(fuc_name):
    arguments = fuc_name[1].split(",")
    var_list = [remove_unnecessary_chars(argument.split(" ")[-1]) for argument in arguments]
    array_dim_list = [remove_empty_string(argument.split(" ")[:-1]) for argument in arguments]
    array_index_list = [i for (i, item) in enumerate(array_dim_list) if 'array' in item[0]]
    
    output_index_list = [i for i in array_index_list if 'output' in var_list[i]]
    array_index_list = [i for i in array_index_list if i not in output_index_list]
    return var_list, array_dim_list, array_index_list, output_index_list

def make_backward_method(output_list):
    string_dict = {0: 'graph', 2: 'op', 3: 'reverse', 5: 'norm'}
    write_string = (f'{INDENTATION}@staticmethod' '\n'
                    f'{INDENTATION}def backward(ctx, dZ):' '\n')
    write_string += f'{INDENTATION*2}pass #must be implemented\n'
    return write_string

def make_res_statements(num_outputs, output_list, string_dict, function_name):
    output_indeces = [i for (i, arg) in enumerate(output_list) if sum('output' in str(item) for item in arg) >= 1]
    result_string = ", ".join(f"res{i+1}" for i in range(num_outputs)) if num_outputs > 1 else "res" #string with list of results
    write_string = f'{INDENTATION*2}{result_string} = gp_apis.gp_{function_name}({make_arguments(output_list, string_dict)})\n'
    write_string += f'{INDENTATION*2}ctx.backward_cache = None #must be implemented\n'
    write_string += f'{INDENTATION}return {result_string}\n'
    return write_string

def make_forward_method(output_list, function_name):
    string_dict = {0: 'graph', 2: 'op', 3: 'reverse', 5: 'norm'}
    write_string = (f'{INDENTATION}@staticmethod' '\n'
                    f'{INDENTATION}def forward(ctx, ')
    write_string += f'{make_arguments(output_list, string_dict)}):\n'
    outputs = [arg for arg in output_list if sum('output' in str(item) for item in arg) >= 1] #get outputs from arguments
    write_string += make_res_statements(len(outputs), output_list, string_dict, function_name)
    return write_string

#generate the class code itself
def generate_class_code(line_string):
    string_sep = line_string.split("{")
    fuc_var = string_sep[0].split("(")
    function_name = get_fuc_name(fuc_var)
    var_list, array_dim_list, array_index_list, output_index_list = fuc_var_class(fuc_var)
    output_list = get_arguments(var_list, array_dim_list, output_index_list, array_index_list) #get func arguments
    
    write_string = f'class {function_name}_api(th.autograd.Function):\n'
    write_string += make_forward_method(output_list, function_name) + '\n'
    write_string += make_backward_method(output_list) + '\n'
    
    return write_string

#generate the wrapper function around the class
def generate_wrapper_function(line_string):
    string_dict = {0: 'graph', 2: 'op', 3: 'reverse', 5: 'norm'}
    string_sep = line_string.split("{")
    fuc_var = string_sep[0].split("(")
    function_name = get_fuc_name(fuc_var)
    var_list, array_dim_list, array_index_list, output_index_list = fuc_var_class(fuc_var)
    output_list = get_arguments(var_list, array_dim_list, output_index_list, array_index_list) #get func arguments
    
    write_string = f'def {function_name}({make_arguments(output_list, string_dict)}):\n'
    write_string += f'{INDENTATION}return {function_name}_api.apply({make_arguments(output_list, string_dict)})\n'
    
    return write_string

#generate the overall code for a line in the input file
def generate_code(line_string):
    write_string = generate_class_code(line_string)
    write_string += generate_wrapper_function(line_string) + '\n'
    return write_string

#overall function to generate full file
def generate_class_file(input_file, output_file):
    write_string = ('import torch as th' '\n'
                    'import gp_apis' '\n\n')
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    write_string += ''.join(generate_code(line) for line in lines)
    with open(output_file, 'w') as file:
        file.write(write_string)