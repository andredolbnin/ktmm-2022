import ctypes as c
import numpy as np
import multiprocessing as mp


class MultiprocessingVerlet:
    
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
        

    def acceleration(self, r, start, end):
        a = np.zeros((end - start, 2), dtype = np.float64)
        for i in range(start, end):
            a_i = self.G * self.M * (self.c - r[i]) / np.linalg.norm(self.c - r[i]) ** 3
            for j in range(self.N):
                if i == j: continue
                a_i += self.G * self.m[j] * (r[j] - r[i]) / np.linalg.norm(r[j] - r[i]) ** 3
            a[i - start] = a_i 
        return a
    

    def next_r(self, r, v, a):
        return r + v * self.t + 0.5 * a * self.t * self.t


    def next_v(self, v, a, next_a):
        return v + 0.5 * (a + next_a) * self.t


    def part1(self, sharedRes, Rh, Vh, Ah, sharedR, idx, q1, q2):
        tmp0 = np.frombuffer(sharedR.get_obj())
        shR = tmp0.reshape((self.N, 2))
        
        tmp1 = np.frombuffer(sharedRes.get_obj())
        shRes = tmp1.reshape((self.iters_num, self.N, 2))
        
        for i in range(self.iters_num - 1):
            Rh[i + 1] = self.next_r(Rh[i], Vh, Ah)
            shR[:idx] = Rh[i + 1]
            q1.put("done")
            q2.get()
            shRes[i + 1] = shR
            nextAh = self.acceleration(shR, 0, idx)
            nextVh = self.next_v(Vh, Ah, nextAh)
            Vh = np.copy(nextVh)
            Ah = np.copy(nextAh)
        return


    def part2(self, Rh, Vh, Ah, sharedR, idx, q1, q2):
        tmp0 = np.frombuffer(sharedR.get_obj())
        shR = tmp0.reshape((self.N, 2))
        
        for i in range(self.iters_num - 1):
            Rh[i + 1] = self.next_r(Rh[i], Vh, Ah)
            shR[idx:] = Rh[i + 1]
            q2.put("done")
            q1.get()
            nextAh = self.acceleration(shR, idx, self.N)
            nextVh = self.next_v(Vh, Ah, nextAh)
            Vh = np.copy(nextVh)
            Ah = np.copy(nextAh)
        return


    def run(self):
        """идея - поделить тела на два процесса, для текущего R
           использовать mp.Array (shared memory), запись в него
           синхронизровать сообщениями через очереди"""
           
        sharedR = mp.Array(c.c_double, self.N * 2)
        sharedRes = mp.Array(c.c_double, self.iters_num * self.N * 2)
        
        R = np.zeros((self.iters_num, self.N, 2), dtype = np.float64)
        R[0] = self.r0
        V = self.v0
        A = self.acceleration(self.r0, 0, self.N)

        q1 = mp.Queue()
        q2 = mp.Queue()

        midN = int(np.ceil(self.N / 2))

        p1 = mp.Process(target = self.part1, args = (sharedRes, R[:, :midN], V[:midN], A[:midN], 
                                                      sharedR, midN, q1, q2))
        p2 = mp.Process(target = self.part2, args = (R[:, midN:], V[midN:], A[midN:], 
                                                      sharedR, midN, q1, q2))

        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
        
        p1.kill()
        p2.kill()
        
        q1.close()
        q1.join_thread()
        
        q2.close()
        q2.join_thread()
        
        tmp = np.frombuffer(sharedRes.get_obj())
        result = tmp.reshape((self.iters_num, self.N, 2))
        result[0] = self.r0
        
        return result
