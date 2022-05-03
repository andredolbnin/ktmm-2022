import time
import numpy as np
import matplotlib.pyplot as plt

from PurePythonVerlet import PurePythonVerlet
from MultiprocessingVerlet import MultiprocessingVerlet


if __name__ == "__main__":
    t = pow(10, 6) * 0.2
    iters_num = 100
    
    c = np.array([0.0, 0.0])
    M = 1.9 * pow(10, 30)
    
    times1 = []
    times2 = []
    
    N_list = [50, 100, 150, 200]
    
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
        
    #plt.style.use("default")
    plt.figure()
    plt.plot(N_list, times1, "-ro", linewidth = 2, label = "python")
    plt.plot(N_list, times2, "-bo", linewidth = 2, label = "multiprocessing")
    plt.title("Сравнение времени (доп)")
    plt.xlabel("N")
    plt.ylabel("Время")
    plt.legend()
    plt.grid()
    
    plt.figure()
    pr1 = np.divide(times1, times1, casting = "same_kind")
    pr2 = np.divide(times1, times2, casting = "same_kind")
    plt.plot(N_list,pr1, "-ro", linewidth = 2, label = "python")
    plt.plot(N_list, pr2, "-bo", linewidth = 2, label = "multiprocessing")
    plt.title("Сравнение ускорения (доп)")
    plt.xlabel("N")
    plt.ylabel("Ускорение")
    plt.legend()
    plt.grid()

    plt.show()
