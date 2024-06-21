import pyopencl as cl
import numpy as np

# Initialisation de OpenCL
platform = cl.get_platforms()[0]
device = platform.get_devices(cl.device_type.GPU)[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Définition du kernel OpenCL
kernel_code = """
__kernel void add(__global const float* a, __global const float* b, __global float* c) {
    int gid = get_global_id(0);
    c[gid] = a[gid] + b[gid];
}
"""
program = cl.Program(context, kernel_code).build()

# Données d'entrée
a = np.array([1, 2, 3, 4, 5], dtype=np.float32)
b = np.array([5, 4, 3, 2, 1], dtype=np.float32)
c = np.empty_like(a)

# Allocation de mémoire sur le GPU
a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a)
b_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=b)
c_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, c.nbytes)

# Exécution du kernel
program.add(queue, a.shape, None, a_buf, b_buf, c_buf)

# Récupération des résultats
cl.enqueue_copy(queue, c, c_buf).wait()
print("Résultat de l'addition sur GPU:", c)
