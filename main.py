import generate_pybind_code as gp
import generate_header_code as gh
import generate_gp_apis_code as gg




gg.generate_binding_file("kernel.dsl", "gp_apis.py", 0)
gg.generate_binding_file("kernel.dsl", "gp_apis_gpu.py", "cuda")
gh.generate_header_file("kernel.dsl")
gp.generate_binding_file("kernel.dsl", "generated_pybind.h")
print("finished!")
