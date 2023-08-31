#get function name
def get_fuc_name(fuc_var):
    return fuc_var[0].split(" ")[-1]

#remove empty strings from a list of strings
def remove_empty_string(string_list):
    return [item for item in string_list if item != '']

#remove unnecessary characters (newline and closing parenthesis) from string
def remove_unnecessary_chars(string):
    for char in ['\n', ')']:
        if char in string:
            string = string.replace(char, '')
    return string

#break function info down
def fuc_var_class(function_info):
    arguments = function_info[1].split(',')
    var_list = [remove_unnecessary_chars(item.split(' ')[-1]) for item in arguments]
    array_dim_list = [remove_empty_string(item.split(' ')[:-1]) for item in arguments]
    array_index_list = [i for (i, item) in enumerate(array_dim_list) if 'array' in item[0]]
    return var_list, array_dim_list, array_index_list

#get dimension of element in `array_dim_list`
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

#create the definition
def create_definition(output_list, function_name):
    write_string = f'm.def("{function_name}",[]('
    argument_dict = {0: "graph_t& graph", 2: "op_t op", 3: "bool reverse", 4: "bool norm"}
    for item in output_list:
        if item[0] in argument_dict:
            write_string += f'{argument_dict[item[0]]}, '
        elif item[0] == 1:
            write_string += f'py::capsule& {item[1]}, '
    write_string = write_string[:-2] + "){\n"
    return write_string

#create the transfrom code
def create_transform_code(output_list, write_string, var_list, array_index_list, function_name):
    for each in output_list:
        if each[0] == 1 and each[2] in [1, 2, 3]:
            write_string += f'        array{each[2]}d_t<float> {each[1]}_array = capsule_to_array{each[2]}d('
            write_string += f'{each[1].replace("_array", "")});\n'
    
    write_string += f'    return {function_name}('
    for (i, var_list_item) in enumerate(var_list):
        if i in array_index_list:
            write_string += f'{var_list_item}_array, '
        #elif var_list_item == 'op':
        #    write_string += f'(op_t)op, '
        else:
            write_string += f'{var_list_item}, '
    return write_string[:-3] + ");\n    }\n  );\n"

#primary generation function
def generate_pybind_code(all_string):
    string_sep = all_string.split("{")
    fuc_var = string_sep[0].split("(")
    function_name = get_fuc_name(fuc_var)
    var_list, array_dim_list, array_index_list = fuc_var_class(fuc_var) #get initial function information
    output_list = record_num_class(var_list, array_index_list, array_dim_list) #get function args
    write_string = create_definition(output_list, function_name) #create initial definition
    write_string = create_transform_code(output_list, write_string, var_list, array_index_list, function_name) #create transform code
    return write_string
    
def generate_binding_file(input_file, output_file):
    write_string = "inline void export_kernel(py::module &m) { \n"
    with open(input_file, 'r') as file:
        lines = file.readlines()
    write_string += ''.join(f'    {generate_pybind_code(line)}' for line in lines) + '}'
    with open(output_file, 'w') as file:
        file.write(write_string)
