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
        a = []
        for i in range(self.N):
            tmp = 0
            for j in range(self.N):
                if i == j: continue
                tmp += self.G * self.m[j] * (r[j] - r[i]) / np.linalg.norm(r[j] - r[i]) ** 3
            tmp += self.G * self.M * (self.c - r[i]) / np.linalg.norm(self.c - r[i]) ** 3
            a.append(tmp)
        return np.array(a, dtype = np.float64)

    def next_r(self, r, v, a):
        return r + v * self.t + 0.5 * a * self.t * self.t

    def next_v(self, v, a, next_a):
        return v + 0.5 * (a + next_a) * self.t

    def run(self):
        R = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        V = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        A = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)

        R[0] = self.r0
        V[0] = self.v0
        A[0] = self.acceleration(self.r0)

        for i in range(self.iters_num - 1):
            R[i + 1] = self.next_r(R[i], V[i], A[i])
            A[i + 1] = self.acceleration(R[i + 1])
            V[i + 1] = self.next_v(V[i], A[i], A[i + 1])

        return R
