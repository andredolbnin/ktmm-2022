import cython
import numpy as np
cimport numpy as np


cdef class CythonVerlet:
    
    cdef double t
    cdef int N
    cdef double M
    cdef int iters_num
    cdef double G
    
    def __init__(CythonVerlet self, double t, int N, double M, int iters_num):
        self.t = t
        self.N = N
        self.M = M
        self.iters_num = iters_num
        self.G = 6.6743 * pow(10, -11)
        

    cpdef acceleration(CythonVerlet self, np.ndarray[np.float64_t, ndim = 2] r,
                       np.ndarray[np.float64_t, ndim = 1] m, np.ndarray[np.float64_t, ndim = 1] c):
        cdef np.ndarray[np.float64_t, ndim = 2] a = np.zeros((self.N, 2))
        for i in range(self.N):
            a_i = self.G * self.M * (c - r[i]) / np.linalg.norm(c - r[i]) ** 3
            for j in range(self.N):
                if i == j: continue
                a_i += self.G * m[j] * (r[j] - r[i]) / np.linalg.norm(r[j] - r[i]) ** 3
            a[i] = a_i 
        return a
    

    cpdef next_r(CythonVerlet self, np.ndarray[np.float64_t, ndim = 2] r, 
                 np.ndarray[np.float64_t, ndim = 2] v, np.ndarray[np.float64_t, ndim = 2] a):
        return r + v * self.t + 0.5 * a * self.t * self.t
    

    cpdef next_v(CythonVerlet self, np.ndarray[np.float64_t, ndim = 2] v, 
                 np.ndarray[np.float64_t, ndim = 2] a, np.ndarray[np.float64_t, ndim = 2] next_a):
        return v + 0.5 * (a + next_a) * self.t
    

    cpdef run(CythonVerlet self, np.ndarray[np.float64_t, ndim = 1] m, np.ndarray[np.float64_t, ndim = 1] c, 
              np.ndarray[np.float64_t, ndim = 2] r0, np.ndarray[np.float64_t, ndim = 2] v0):
        cdef np.ndarray[np.float64_t, ndim = 3] R = np.zeros((self.iters_num, self.N, 2))
        R[0] = r0
        cdef np.ndarray[np.float64_t, ndim = 2] V = v0
        cdef np.ndarray[np.float64_t, ndim = 2] A = self.acceleration(r0, m, c)

        for i in range(self.iters_num - 1):
            R[i + 1] = self.next_r(R[i], V, A)
            nextA = self.acceleration(R[i + 1], m, c)
            nextV = self.next_v(V, A, nextA)
            V = np.copy(nextV)
            A = np.copy(nextA)

        return R