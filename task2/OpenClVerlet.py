import numpy as np
import pyopencl as cl


class OpenClVerlet:
    
    def __init__(self, t, m, N, c, M, r0, v0, iters_num):
        self.t = t
        self.m = m
        self.N = N
        self.c = c
        self.M = M
        self.r0 = r0
        self.v0 = v0
        self.iters_num = iters_num
        self.G = 6.6743 * pow(10, -11)
        

    def run(self):
        platform = cl.get_platforms()[0] # nvidia
        device = platform.get_devices()[0]
        ctx = cl.create_some_context([device])
        queue = cl.CommandQueue(ctx)

        mf = cl.mem_flags
        
        loc_mem = cl.LocalMemory(1)
        
        m_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.m)
        c_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = self.c)
        
        V = self.v0
        A = np.zeros((self.N, 2), dtype = np.float64)
        
        V_cl = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = V)
        A_cl = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = A)
        
        nextV = np.zeros((self.N, 2), dtype = np.float64)
        nextA = np.zeros((self.N, 2), dtype = np.float64)
        
        nextV_cl = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = nextV)
        nextA_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = nextA)

        prg = cl.Program(ctx, """
                    
                    double next_r(const double r,
                                  const double v,
                                  const double a,
                                  const double t) 
                    {
                        return r + v * t + 0.5 * a * t * t;
                    }   
                    
                    double next_v(const double v,
                                  const double a,
                                  const double next_a,
                                  const double t) 
                    {
                        return v + 0.5 * (a + next_a) * t;
                    }    
                                 
                                 
                    __kernel void run(__local double *loc_mem,
                                      __global double *Res,
                                      __global double *m,
                                      __global double *c,
                                      __global double *V,
                                      __global double *A,
                                      __global double *nextV,
                                      __global double *nextA,
                                      const double time,
                                      const unsigned N,
                                      const double M,
                                      const unsigned iters_num,
                                      const double G)
                    {   
                        int GID = get_global_id(1);
                        int dim = 2;
                        int num = dim * N;
                        
                        double norm = sqrt(pow(c[0] - Res[GID * dim + 0], 2) + pow(c[1] - Res[GID * dim + 1], 2));
                        for (int d = 0; d < dim; d++) {
                            double a = G * M * (c[d] - Res[GID * dim + d]) / pow(norm, 3);
                            for (int n1 = 0; n1 < N; n1++) {
                                if (n1 == GID) continue;
                                double norm1 = sqrt(pow(Res[n1 * dim + 0] - Res[GID * dim + 0], 2) + pow(Res[n1 * dim + 1] - Res[GID * dim + 1], 2));
                                for (int d1 = 0; d1 < dim; d1++) {
                                    a += G * m[n1] * (Res[n1 * dim + d1] - Res[GID * dim + d1]) / pow(norm1, 3);
                                }
                            
                            }     
                            A[GID * dim + d] = a;
                        }
                        barrier(CLK_GLOBAL_MEM_FENCE);
                        
                        for (int t = 0; t < iters_num - 1; t++) {
                            //1
                            for (int d = 0; d < dim; d++) {
                                double r = Res[t * num + GID * dim + d];
                                double v = V[GID * dim + d];
                                double a = A[GID * dim + d];
                                Res[(t + 1) * num + GID * dim + d] = next_r(r, v, a, time);
                            }    
                            barrier(CLK_GLOBAL_MEM_FENCE);
                            
                            //2
                            double norm = sqrt(pow(c[0] - Res[(t + 1) * num + GID * dim + 0], 2) + pow(c[1] - Res[(t + 1) * num + GID * dim + 1], 2));
                            for (int d = 0; d < dim; d++) {
                                double a = G * M * (c[d] - Res[(t + 1) * num + GID * dim + d]) / pow(norm, 3);
                                for (int n1 = 0; n1 < N; n1++) {
                                    if (n1 == GID) continue;
                                    double norm1 = sqrt(pow(Res[(t + 1) * num + n1 * dim + 0] - Res[(t + 1) * num + GID * dim + 0], 2) + pow(Res[(t + 1) * num + n1 * dim + 1] - Res[(t + 1) * num + GID * dim + 1], 2));
                                    for (int d1 = 0; d1 < dim; d1++) {
                                        a += G * m[n1] * (Res[(t + 1) * num + n1 * dim + d1] - Res[(t + 1) * num + GID * dim + d1]) / pow(norm1, 3);
                                    }
                                }   
                                nextA[GID * dim + d] = a;
                            }
                            barrier(CLK_GLOBAL_MEM_FENCE);
                            
                            //3
                            for (int d = 0; d < dim; d++) {
                                double v = V[GID * dim + d];
                                double a = A[GID * dim + d];
                                double next_a = nextA[GID * dim + d];
                                nextV[GID * dim + d] = next_v(v, a, next_a, time);             
                            }   
                            barrier(CLK_GLOBAL_MEM_FENCE);
                            
                            //4
                            for (int d = 0; d < dim; d++) {
                                V[GID * dim + d] = nextV[GID * dim + d];
                                A[GID * dim + d] = nextA[GID * dim + d];
                            }
                            
                            barrier(CLK_GLOBAL_MEM_FENCE);
                            
                        }
                    }
        
                """).build()
        
        R_tmp = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        R_tmp[0] = self.r0
        Res_g = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf = R_tmp)

        knl = prg.run
        completeEvent = knl(queue, R_tmp.shape, None, loc_mem, Res_g, m_cl, c_cl, V_cl, A_cl, nextV_cl, nextA_cl,
            np.double(self.t), np.int32(self.N), np.double(self.M), np.int32(self.iters_num),
            np.double(self.G))

        Res_np = np.empty_like(R_tmp)
        cl.enqueue_copy(queue, Res_np, Res_g)
        
        # чистим память
        queue.finish()
        m_cl.release()
        c_cl.release()
        V_cl.release()
        A_cl.release()
        nextV_cl.release()
        nextA_cl.release()
        Res_g.release()
        
        return Res_np
