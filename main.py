import generate_pybind_code as gp
import generate_header_code as gh
import generate_gp_apis_code as gg
import generate_class_code as gc



gg.generate_binding_file("kernel.dsl", "gp_apis.py")
gh.generate_header_file("kernel.dsl")
gp.generate_binding_file("kernel.dsl", "generated_pybind.h")
gc.generate_class_file('kernel.dsl', 'generated_classes.py')
print("finished!")
