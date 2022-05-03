import numpy as np
from scipy.integrate import odeint


class OdeintSolver:
    
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
        for i in range(0, self.N * 2, 2):
            tmp = 0
            for j in range(0, self.N * 2, 2):
                if i == j: continue
                d = r[j:j+2] - r[i:i+2]
                tmp += self.G * self.m[j // 2] * d / np.linalg.norm(d) ** 3
            tmp += self.G * self.M * (self.c - r[i:i+2]) / np.linalg.norm(self.c - r[i:i+2]) ** 3
            a.append(tmp)
        return np.ndarray.flatten(np.array(a, dtype = np.float64))
    

    def sys_of_funcs(self, r_v, t):
        res = np.zeros(r_v.shape)
        mid_idx = r_v.size // 2
        r = r_v[:mid_idx]
        v = r_v[mid_idx:]
        res[mid_idx:] = self.acceleration(r)
        res[:mid_idx] = v
        return res
    

    def solve(self):
        t = np.arange(0, self.t * self.iters_num, self.t)
        # odeint не работает с двумерными векторами [x, y], поэтому нужен flatten
        sol_with_v = odeint(self.sys_of_funcs, np.ndarray.flatten(np.concatenate((self.r0, self.v0))), t)
        sol = sol_with_v[:, :self.N * 2] # выкидываем часть со скоростями, shape = (iters_num, 8)
        R = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        R[0] = self.r0
        for i in range(len(sol) - 1):
            tmp = []
            for j in range(0, self.N * 2, 2):
                x = sol[i][j]
                y = sol[i][j + 1]
                tmp.append(np.array([x, y], dtype = np.float64))
            R[i + 1] = np.array(tmp)
        return R
