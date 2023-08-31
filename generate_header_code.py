#generate a header file for a given input file.
#will write to a new file with the same name but a `.h` extension
def generate_header_file(input_file):
    #get output file name
    input_file_name_list = input_file.split(".")
    input_file_name = input_file_name_list[0]
    output_file = input_file_name + ".h"
    
    #read text from input file and add headers to beginning
    output_string = ('#pragma once' '\n'
                     '#include "csr.h"' '\n'
                     '#include "op.h"' '\n\n')

    with open(input_file, 'r') as file:
        output_string += file.read()
    
    #write to output file
    with open(output_file, 'w') as file:
        file.write(output_string)


    with open(input_file, 'r') as file:
     output_string = file.read()

    output_file_cu = input_file_name + ".cu"
    with open(output_file_cu, 'w') as file:
        file.write ('#include "' + output_file + '"\n\n' + output_string.replace(";", "{;}"))
