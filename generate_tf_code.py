INDENTATION = "    "

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

def fuc_var_class(fuc_name):
    arguments = fuc_name[1].split(",")
    var_list = [remove_unnecessary_chars(argument.split(" ")[-1]) for argument in arguments]
    array_dim_list = [remove_empty_string(argument.split(" ")[:-1]) for argument in arguments]
    array_index_list = [i for (i, item) in enumerate(array_dim_list) if 'array' in item[0]]
    
    output_index_list = [i for i in array_index_list if 'output' in var_list[i]]
    array_index_list = [i for i in array_index_list if i not in output_index_list]
    return var_list, array_dim_list, array_index_list, output_index_list

def cal_array_class(array_dim_list, i):
    each_element = array_dim_list[i]
    for i in range(3):
        if str(i+1) in each_element[0]:
            return str(i+1)
    return "10000"

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

#get the function header (ie, `def` plus the name and the arguments)
def make_function_header(function_name, output_list, string_dict):
    write_string = f'def gp_{function_name}('
    num_of_dlpack_index = []
    num_of_dlpack_name = []
    for (j, item) in enumerate(output_list):
        if item[0] in string_dict:
            write_string += f'{string_dict[item[0]]}, '
        elif item[0] == 1:
            num_of_dlpack_index.append(j)
            new_input = item[1].replace("input", "X")
            num_of_dlpack_name.append(new_input)
            write_string += f'{new_input}, '
        elif (item[0] == 4) and (item[2] in range(1, 4)):
            id = item[1].replace("output", "")
            write_string += ', '.join(f'dim{id}_{i}' for i in range(item[2])) + ', '
    write_string = f"{write_string[:-2]}):\n" #remove final comma/space and add ender
    return write_string, num_of_dlpack_index, num_of_dlpack_name

#add dlpack and device lines
def add_dlpack(num_of_dlpack_index, num_of_dlpack_name, write_string):
    for (k, _) in enumerate(num_of_dlpack_index):
        write_string += f'{INDENTATION}{num_of_dlpack_name[k]}_dl = tf.experimental.dlpack.to_dlpack({num_of_dlpack_name[k]})\n'
    return write_string

#declare the tensor allocation
def declare_tensor_allocation(output_index_list, array_dim_list, write_string, function_name):
    for (id, each) in enumerate(output_index_list):
        id = "" if len(output_index_list) == 1 else str(id+1)
        array_class = cal_array_class(array_dim_list, each)
        dimension_string = ', '.join(f'dim{id}_{i}' for i in range(int(array_class)))
        write_string += f'{INDENTATION}res{id} = tf.zeros([{dimension_string}])\n{INDENTATION}res_dl{id} = tf.experimental.dlpack.to_dlpack(res{id})\n'
    write_string += f'{INDENTATION}gpk.{function_name}('
    return write_string

#primary code generation function
def generate_pybind_code(all_string):
    string_dict = {0: 'graph', 2: 'op', 3: 'reverse', 5: 'norm'}
    function_string = all_string.split("{")
    fuc_var = function_string[0].split("(")
    function_name = get_fuc_name(fuc_var)
    var_list, array_dim_list, array_index_list, output_index_list = fuc_var_class(fuc_var)
    
    output_list = get_arguments(var_list, array_dim_list, output_index_list, array_index_list) #get func arguments
    write_string, num_of_dlpack_index, num_of_dlpack_name = make_function_header(function_name, output_list, string_dict) #make header for func
    write_string = add_dlpack(num_of_dlpack_index, num_of_dlpack_name, write_string) #add dlpack and device lines
    write_string += f'{INDENTATION}#declare the output tensor here\n'
    write_string = declare_tensor_allocation(output_index_list, array_dim_list, write_string, function_name) #declare the tensor allocation
    
    flag = 0
    output_tracker = 1 if len(output_index_list) > 1 else ""
    for (i, item) in enumerate(output_list):
        if item[0] in string_dict:
            write_string += f'{string_dict[item[0]]}, '
        elif item[0] == 1:
            write_string += num_of_dlpack_name[flag] + "_dl" + ", "
            flag += 1
        elif item[0] == 4:
            write_string += f"res_dl{output_tracker}, "
            output_tracker = "" if len(output_index_list) == 1 else output_tracker+1
    
    res_string = ", ".join(f"res{i+1}" for (i, _) in enumerate(output_index_list)) if len(output_index_list) > 1 else "res"
    write_string = f'{write_string[:-2]})\n{INDENTATION}return {res_string}\n'
    return write_string

def generate_tf_file(input_file, output_file):
    write_string = ('import tensorlow as tf' '\n'
                    'import kernel as gpk' '\n')
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    write_string += ''.join(generate_pybind_code(line) for line in lines)
    with open(output_file, 'w') as file:
        file.write(write_string)
