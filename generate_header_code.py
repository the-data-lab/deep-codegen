def generate_header_file(input_file):
    input_file_name_list = input_file.split(".")
    input_file_name = input_file_name_list[0]
    output_file = input_file_name + ".h"
    with open(input_file, 'r') as reader:
        lines = reader.readlines()
    output_string = "#pragma once" + "\n" + "#include \"csr.h\"" + "\n" + "#include \"op.h\"" + "\n" + "extern int THD_COUNT;" + '\n'
    for line in lines:
#         print(count)
        output_string = output_string + line
#     print(output_string)
#     print(output_file)
    file1 = open(output_file, 'w')
    file1.write(output_string)
