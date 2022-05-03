import numpy as np
import matplotlib.pyplot as plt

from OdeintSolver import OdeintSolver
from PurePythonVerlet import PurePythonVerlet
from MultiprocessingVerlet import MultiprocessingVerlet
from OpenClVerlet import OpenClVerlet
from CythonVerlet import CythonVerlet


if __name__ == "__main__":
    t = 1
    scale = pow(10, 12)
    iters_num = pow(10, 2)
    
    c = np.array([0.0, 0.0])
    
    G = 6.6743 * pow(10, -11)
    
    m = np.array([1.0243, 0.87, 5.68, 18.986, 0.0064, 0.0597, 0.049, 0.0033],
                  dtype = np.float64) * np.array([pow(10, 26)], dtype = np.float64)
    M = 1.9 * pow(10, 30)
    
    N = 8
    
    r0 = np.array([[4.5, 0.0], [2.8, 0.0], [1.43, 0.0], [0.8, 0.0],
                   [0.23, 0.0], [0.15, 0.0], [0.11, 0.0], [0.057, 0.0]],
                   dtype = np.float64) * scale
    v0 = np.array([[0.0, 5.4], [0.0, 6.8], [0.0, 9.69], [0.0, 13.07],
                   [0.0, 24.13], [0.0, 29.8], [0.0, 35.0], [0.0, 40.0]], #170
                   dtype = np.float64) * pow(10, 3)
    
    odeint_solver = OdeintSolver(t, m, N, c, M, r0, v0, iters_num)
    R0 = odeint_solver.solve()
    
    solver1 = PurePythonVerlet(t, m, N, c, M, r0, v0, iters_num)
    R1 = solver1.run()
    
    solver2 = MultiprocessingVerlet(t, m, N, c, M, r0, v0, iters_num)
    R2 = solver2.run()
    
    solver3 = OpenClVerlet(t, m, N, c, M, r0, v0, iters_num)
    R3 = solver3.run()
    
    solver4 = CythonVerlet(t, N, M, iters_num)
    R4 = solver4.run(m, c, r0, v0)
    
    res1 = np.linalg.norm(R0 - R1) / scale
    res2 = np.linalg.norm(R0 - R2) / scale
    res3 = np.linalg.norm(R0 - R3) / scale
    res4 = np.linalg.norm(R0 - R4) / scale
    
    print(res1)
    print(res2)
    print(res3)
    print(res4)
    
    fig, ax = plt.subplots()
    ax.bar(["python", "multiprocessing", "opencl", "cython"], [res1, res2, res3, res4])
    plt.title("Ошибка по сравнению с Odeint")
    plt.show()
