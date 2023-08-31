import generate_pybind_code as gp
import generate_header_code as gh
import generate_gp_apis_code as gg
import generate_class_code as gc
import generate_tf_code as gt
import generate_sparse_code as gs

#Generate common back-end code
gh.generate_header_file("kernel.dsl")
gp.generate_binding_file("kernel.dsl", "generated_pybind.h")

#Generate Pytorch specific code
gg.generate_binding_file("kernel.dsl", "gp_apis.py")
gc.generate_class_file('kernel.dsl', 'pytorch_apis.py')

#Generate Tensorflow specific code
gt.generate_tf_file('kernel.dsl', 'gp_apis_tf.py')
gs.generate_sparse_file('kernel.dsl', 'tf_apis.py')
print("finished!")
