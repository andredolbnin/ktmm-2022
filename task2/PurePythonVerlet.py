import numpy as np


class PurePythonVerlet:
    
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
        

    def acceleration(self, r):
        a = np.zeros((self.N, 2), dtype = np.float64)
        for i in range(self.N):
            a_i = self.G * self.M * (self.c - r[i]) / np.linalg.norm(self.c - r[i]) ** 3
            for j in range(self.N):
                if i == j: continue
                a_i += self.G * self.m[j] * (r[j] - r[i]) / np.linalg.norm(r[j] - r[i]) ** 3
            a[i] = a_i 
        return a
    

    def next_r(self, r, v, a):
        return r + v * self.t + 0.5 * a * self.t * self.t
    

    def next_v(self, v, a, next_a):
        return v + 0.5 * (a + next_a) * self.t
    

    def run(self):
        R = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        R[0] = self.r0
        V = self.v0
        A = self.acceleration(self.r0)

        for i in range(self.iters_num - 1):
            R[i + 1] = self.next_r(R[i], V, A)
            nextA = self.acceleration(R[i + 1])
            nextV = self.next_v(V, A, nextA)
            V = np.copy(nextV)
            A = np.copy(nextA)

        return R
