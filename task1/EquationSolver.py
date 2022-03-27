import json
import config
import numpy as np
from scipy.integrate import odeint


class EquationSolver:
    def __init__(self, coef_file, sol_file):
        self.sol_file = sol_file
        
        with open(coef_file, 'r') as f:
            data = json.load(f)
            self.c = np.array(list(data['c'].values()), dtype = float)
            lmbd_dict = data["lmbd"]
            self.eps = np.array(list(data["eps"].values()), dtype = float)
            self.A = int(data['A'])
            
        def Qr1234(t):
            return 0
        
        def Qr5(t):
            return self.A * (20 + 3 * np.sin(t / 4))
        
        self.Qr = [Qr1234] * 4 + [Qr5]
            
        with open(config.model_data_file, 'r') as f:
            data = json.load(f)
            self.N = int(data['N'])
            self.Si = np.array(list(data["Si"].values()), dtype = float)
            Sij_info = data["Sij"]
    
        lmbd = np.zeros((self.N, self.N), dtype = float)
        for key in lmbd_dict:
            keys = list(map(int, key.split()))
            lmbd[keys[0] - 1, keys[1] - 1] = lmbd[keys[1] - 1, keys[0] - 1] = lmbd_dict[key]
            
        Sij = np.zeros((self.N, self.N), dtype = float)   
        for key in Sij_info:
            keys = list(map(int, key.split()))
            Sij[keys[0] - 1, keys[1] - 1] = Sij[keys[1] - 1, keys[0] - 1] = Sij_info[key]
            
        self.k = lmbd * Sij
        self.C0 = 5.67
        
        
    def sys_of_funcs(self, T, t):
        res = np.zeros(self.N)
        for i in range(self.N):
            res[i] -= np.sum(self.k[i] * (T[i] - T)) 
            res[i] -= self.C0 * self.eps[i] * self.Si[i] * pow((T[i] / 100), 4)
            res[i] += self.Qr[i](t)
        return res / self.c
    
    
    def solve(self, T = 200):
        init = 20, 20, 20, 20, 24
        N = 2001
        self.t = np.linspace(0, T, N)
        sol = odeint(self.sys_of_funcs, init, self.t)
        with open(self.sol_file, 'w') as f:
            arr = np.column_stack((self.t, sol))
            np.savetxt(f, arr)
