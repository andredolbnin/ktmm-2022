# how to install:
# http://www.minho-kim.com/courses/17sp43.635/pyopencl.html

import numpy as np
import pyopencl as cl

a_np = np.random.rand(50000).astype(np.float32)
b_np = np.random.rand(50000).astype(np.float32)

# создание контекста для GPU
ctx = cl.create_some_context()
# создание очереди команд для работы с контекстом
queue = cl.CommandQueue(ctx)

# memory flags
mf = cl.mem_flags 
# буферы
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)

# код, который будет исполнен на GPU, c (kernel) функцией sum
prg = cl.Program(ctx, """
__kernel void sum(
    __global const float *a_g, __global const float *b_g, __global float *res_g)
{
  int gid = get_global_id(0);
  res_g[gid] = a_g[gid] + b_g[gid];
}
""").build()

# буфер на запись
res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)

# получаем kernel
knl = prg.sum
knl(queue, a_np.shape, None, a_g, b_g, res_g)

res_np = np.empty_like(a_np)
# копируем память устройства в память хоста
cl.enqueue_copy(queue, res_np, res_g)

# Check on CPU with Numpy
print(res_np - (a_np + b_np))
print(np.linalg.norm(res_np - (a_np + b_np)))
assert np.allclose(res_np, a_np + b_np)
