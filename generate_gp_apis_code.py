def get_fuc_name(fuc_var):
    result = fuc_var[0].split(" ")
    return result[-1]

def fuc_var_class(c):
    d = c[1].split(",")
    var_list = []
    array_dim_list = []
    array_index_list = []
    output_index_list = []
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
            
    # output_index_list refers to the index of ouput
    for each in array_index_list:
        temp = var_list[each]
        if "output" in temp:
            output_index_list.append(each)
            array_index_list.remove(each)
            
        

        
    return var_list, array_dim_list, array_index_list, output_index_list


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


def generate_pybind_code(all_string, gpu):
#         print(type(a))
        #print(a)
        string_sep = all_string.split("{")
        fuc_var = string_sep[0].split("(")
        function_name = get_fuc_name(fuc_var)
#         print(fuc_var)
        var_list, array_dim_list, array_index_list, output_index_list = fuc_var_class(fuc_var)
#         print(var_list)
#         print(array_dim_list)
#         print(array_index_list)
#         print(output_index_list)
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
            elif i in output_index_list:
                temp1 = [4, var_list[i]]
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
                    output_list.append([5, "norm"])
                
        write_string = "def " + "gp_" + function_name + "(" 
        num_of_dlpack_index = []
        num_of_dlpack_name = []
        for j in range(len(output_list)):
            each = output_list[j]
#             print(each)
            if each[0] == 0:
                write_string = write_string + "graph, "
            elif each[0] == 1:
                #print(each[1])
                #print(j)
                num_of_dlpack_index.append(j)
                #new_input = each[1].replace("_array", str(j))
                new_input = each[1] +  "1"
                num_of_dlpack_name.append(new_input)
                write_string = write_string + new_input + ", "
            elif each[0] == 2:
                write_string = write_string + "op, "
            elif each[0] == 3:
                write_string = write_string + "reverse, "
            elif each[0] == 5:
                write_string = write_string + "norm, "
            elif each[0] == 4:
                if each[2] == 2:
                    write_string = write_string + "dim0, dim1, "
                elif each[2] == 3:
                     write_string = write_string + "dim0, dim1, dim2, "
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string + "):"
        write_string = write_string + "\n"
#         print("ha,,,", num_of_dlpack_index)
        indentation = "    "
        for k in range(len(num_of_dlpack_index)):
            write_string = write_string + indentation + num_of_dlpack_name[k] + "_dl = th.utils.dlpack.to_dlpack("
            write_string = write_string + num_of_dlpack_name[k] + ")" + "\n"
        if gpu != 0:
              write_string = write_string + indentation + "cuda0 = th.device('" + gpu + "')\n"
        # declare the tensor allocation
#         print(output_index_list)
        for each in output_index_list:
            array_class = cal_array_class(array_dim_list, each)
#             print("ha", array_dim_list[each])
#             print("ha1", array_class)
            if array_class == str(2):
                if gpu != 0:
                    write_string = write_string + indentation + "res = th.zeros(dim0, dim1, device = cuda0)\n" + indentation + "res_dl = th.utils.dlpack.to_dlpack(res)\n"
                else:
                    write_string = write_string + indentation + "res = th.zeros(dim0, dim1)\n" + indentation + "res_dl = th.utils.dlpack.to_dlpack(res)\n"
            elif array_class == str(3):
                if gpu != 0:
                    write_string = write_string + indentation + "res = th.zeros(dim0, dim1, dim2, device = cuda0)\n" + indentation + "res_dl = th.utils.dlpack.to_dlpack(res)\n"
                else:
                    write_string = write_string + indentation + "res = th.zeros(dim0, dim1, dim2)\n" + indentation + "res_dl = th.utils.dlpack.to_dlpack(res)\n"
            
            
        write_string = write_string + indentation + "gpk" + "." + function_name + "("
        
#         print(num_of_dlpack_name)
        flag = 0
#         print(output_list)
        for l in range(len(output_list)):
            each = output_list[l]
#             print(each)
            if each[0] == 0:
                write_string = write_string + "graph, "
            elif each[0] == 1:
                #print(each[1])
#                 print("lll",l)
#                 index = num_of_dlpack_index[l]
#                 print(index)
                write_string = write_string + num_of_dlpack_name[flag] + "_dl" + ", "
                flag = flag + 1
            elif each[0] == 2:
                write_string = write_string + "op, "
            elif each[0] == 3:
                write_string = write_string + "reverse, "
            elif each[0] == 4:
                write_string = write_string + "res_dl, "
            elif each[0] == 5:
                write_string = write_string + "norm, "
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string.rstrip(write_string[-1])
        write_string = write_string + ")"
        write_string = write_string + "\n"
        # write the output variable
#         print(output_list[result_index])
#         for each in output_index_list:
#             out_put_var = output_list[each]
# #         print("333", out_put_var[0])
#         if out_put_var[0] == 0:
#             result = "graph, "
#         elif out_put_var[0] == 1:
#             #print(each[1])
#             #new_input = each[1].replace("_array", str(j))
#             result = out_put_var[1].replace("_array", "")
            
#         elif out_put_var[0] == 2:
#             result = "op, "
#         elif out_put_var[0] == 3:
#             result = "reverse"

#         print("888",result)
        write_string = write_string + indentation + "return res \n"
#         print(write_string)
        return write_string



def generate_binding_file(input_file, output_file, gpu):
    write_string = "import torch as th \nimport torch.utils.dlpack \nimport kernel as gpk \n"
    with open(input_file, 'r') as reader:
        lines = reader.readlines()
    #output_string = "#pragma once" + "\n" + "#include \"csr.h\"" + "\n" + "#include \"op.h\"" + "\n" + "extern int THD_COUNT;" + '\n'
    
    for line in lines:
#         print(count)
        output_string = generate_pybind_code(line, gpu)
        write_string = write_string + output_string
#     write_string = write_string + "}"
    # print(write_string)
#     print(output_file)
        file1 = open(output_file, 'w')
        file1.write(write_string)
    
