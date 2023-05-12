def get_fuc_name(fuc_var):
    result = fuc_var[0].split(" ")
    return result[-1]

def fuc_var_class(c):
    d = c[1].split(",")
    var_list = []
    array_dim_list = []
    array_index_list = []
#     print("dd",d)
    for each in d:
        temp = each.split(" ")
        var_list.append(temp[-1])
        array_dim_list.append(temp[:-1])

    # remove the "" for array_dim_list
    for i in range(len(array_dim_list)):
        temp = array_dim_list[i]
        temp1 = []
#         print("temp", temp)
        for j in range(len(temp)):
            if temp[j] != "":
                temp1.append(temp[j])
        array_dim_list[i] = temp1
        
        
    # remove the "\n" ")" for var_list
    for i in range(len(var_list)):
        temp = var_list[i]
        if "\n" in temp:
            temp = temp.replace("\n", "")
        if ")" in temp:
            temp = temp.replace(")", "")
        var_list[i] = temp
        
    
    for i in range(len(array_dim_list)):
        temp = array_dim_list[i]
        if "array" in temp[0]:
            array_index_list.append(i)
        

        
    return var_list, array_dim_list, array_index_list


def cal_array_class(array_dim_list, i):
    each_element = array_dim_list[i]
    
    if "1" in each_element[0]:
        return "1"
    elif "2" in each_element[0]:
        return "2"
    elif "3" in each_element[0]:
        return "3"
    else:
        return "10000"


def generate_pybind_code(all_string):
#         print(type(a))
        #print(a)
        string_sep = all_string.split("{")
        fuc_var = string_sep[0].split("(")
        function_name = get_fuc_name(fuc_var)
        var_list, array_dim_list, array_index_list = fuc_var_class(fuc_var)
#         print(var_list)
#         print(array_dim_list)
#         print(array_index_list)
        # record the num of class
        class_choice = ["graph", "array", "op", "reverse"]
        output_list = []
        for i in range(len(var_list)):
            if i in array_index_list:
                
                temp1 = [1, var_list[i]]
#                 print(array_dim_list[i])
                array_class = cal_array_class(array_dim_list, i)
                temp1.append(int(array_class))
                output_list.append(temp1)
                
                
            else:
#             print(i)
                if "graph" in var_list[i]:
                    output_list.append([0, "graph"])
                elif "op" in var_list[i]:
                    output_list.append([2, "op"])
                elif "reverse" in var_list[i]:
                    output_list.append([3, "reverse"])
                elif "norm" in var_list[i]:
                    output_list.append([4, "norm"])
            # deal with the array
                
        write_string = "m.def(\"" + function_name + "\",[]("
        # create the definition
#         print("aaa", output_list)
        for each in output_list:
#             print(each)
            if each[0] == 0:
                write_string = write_string + "graph_t& graph, "
            elif each[0] == 1:
                write_string = write_string + "py::capsule& "
                #print(each[1])
                new_input = each[1] + ", "
                write_string = write_string + new_input
            elif each[0] == 2:
                write_string = write_string + "op_t op, "
            elif each[0] == 3:
                write_string = write_string + "bool reverse, "
            elif each[0] == 4:
                write_string = write_string + "bool norm, "
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string + "){\n"
        # create the transfrom code
        for each in output_list:
#             print(each[0])
            if each[0] == 1:
#                 print("ha")
#                 print(type(each[2]))
#                 print(each[2])
                if each[2] == int(1):
                    
                    write_string = write_string + "        array1d_t<float> " + each[1] + "_array = capsule_to_array1d("
                    new_input = each[1].replace("_array", "")
                    write_string = write_string + new_input + ");\n" 
                
                if each[2] == int(2):
                    write_string = write_string + "        array2d_t<float> " + each[1] + "_array = capsule_to_array2d("
                    new_input = each[1].replace("_array", "")
                    write_string = write_string + new_input + ");\n" 
                    
                if each[2] == int(3):
                    write_string = write_string + "        array3d_t<float> " + each[1] + "_array = capsule_to_array3d("
                    new_input = each[1].replace("_array", "")
                    write_string = write_string + new_input + ");\n"
                
            else:
                continue
        
        #print(function_name)
        write_string = write_string + "    return " + function_name + "("
        for i in range(len(var_list)):
            if i in array_index_list:
                write_string = write_string + var_list[i] + "_array, "
            else:
                if var_list[i] == "op":
                    write_string = write_string + "(op_t)" + var_list[i] + ", "
                else:
                    write_string = write_string + var_list[i] + ", "
        
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string + ");\n    }\n  );\n"
        
#         print(write_string)
        # write the pybind code to output file
#         file1 = open(output_file, 'w')
#         file1.write(write_string)
        return write_string
        
                
def generate_binding_file(input_file, output_file):
    write_string = "inline void export_kernel(py::module &m) { \n"
    with open(input_file, 'r') as reader:
        lines = reader.readlines()
    #output_string = "#pragma once" + "\n" + "#include \"csr.h\"" + "\n" + "#include \"op.h\"" + "\n" + "extern int THD_COUNT;" + '\n'
    
    for line in lines:
#         print(count)
        output_string = generate_pybind_code(line)
        write_string = write_string + "    " + output_string
    write_string = write_string + "}"
    #print(write_string)
#     print(output_file)
    file1 = open(output_file, 'w')
    file1.write(write_string)                
