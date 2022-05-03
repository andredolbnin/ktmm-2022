import time
import numpy as np
import matplotlib.pyplot as plt

from PurePythonVerlet import PurePythonVerlet
from MultiprocessingVerlet import MultiprocessingVerlet
from OpenClVerlet import OpenClVerlet
from CythonVerlet import CythonVerlet


if __name__ == "__main__":
    t = pow(10, 6) * 0.2
    iters_num = 20
    
    c = np.array([0.0, 0.0])
    M = 1.9 * pow(10, 30)
    
    times1 = []
    times2 = []
    times3 = []
    times4 = []
    
    N_list = [50, 100, 150]
    
    for N in N_list:
        m = np.random.rand(N)
        
        r0 = np.random.rand(N, 2)
        v0 = np.random.rand(N, 2)
        
        s1 = time.time()
        solver1 = PurePythonVerlet(t, m, N, c, M, r0, v0, iters_num)
        R1 = solver1.run()
        times1.append(time.time() - s1)
        
        s2 = time.time()
        solver2 = MultiprocessingVerlet(t, m, N, c, M, r0, v0, iters_num)
        R2 = solver2.run()
        times2.append(time.time() - s2)
        
        s3 = time.time()
        solver3 = OpenClVerlet(t, m, N, c, M, r0, v0, iters_num)
        R3 = solver3.run()
        times3.append(time.time() - s3)
        
        s4 = time.time()
        solver4 = CythonVerlet(t, N, M, iters_num)
        R4 = solver4.run(m, c, r0, v0)
        times4.append(time.time() - s4)
        
    #plt.style.use("default")
    plt.figure()
    plt.plot(N_list, times1, "-ro", linewidth = 2, label = "python")
    plt.plot(N_list, times2, "-bo", linewidth = 2, label = "multiprocessing")
    plt.plot(N_list, times3, "-go", linewidth = 2, label = "opencl")
    plt.plot(N_list, times4, "-yo", linewidth = 2, label = "cython")
    plt.title("Сравнение времени")
    plt.xlabel("N")
    plt.ylabel("Время")
    plt.legend()
    plt.grid()
    
    plt.figure()
    pr1 = np.divide(times1, times1, casting = "same_kind")
    pr2 = np.divide(times1, times2, casting = "same_kind")
    pr3 = np.divide(times1, times3, casting = "same_kind")
    pr4 = np.divide(times1, times4, casting = "same_kind")
    plt.plot(N_list,pr1, "-ro", linewidth = 2, label = "python")
    plt.plot(N_list, pr2, "-bo", linewidth = 2, label = "multiprocessing")
    plt.plot(N_list, pr3, "-go", linewidth = 2, label = "opencl")
    plt.plot(N_list, pr4, "-yo", linewidth = 2, label = "cython")
    plt.title("Сравнение ускорения")
    plt.xlabel("N")
    plt.ylabel("Ускорение")
    plt.legend()
    plt.grid()

    plt.show()
    