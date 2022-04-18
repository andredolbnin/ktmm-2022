import numpy as np

from OdeintSolver import OdeintSolver
from PurePythonVerlet import PurePythonVerlet

t = pow(10, 7) * 1.5
scale = pow(10, 12)
iters_num = pow(10, 2)

w = 5 * scale
h = 5 * scale

c = np.array([0.0, 0.0])

m = np.array([1.0243, 0.87, 5.68, 18.986], dtype = np.float64) * pow(10, 26)
M = 1.9 * pow(10, 30)

N = 4

r0 = np.array([[4.5, 0.1], [2.8, 0.2], [1.43, 0.3], [0.8, 0.4]], dtype = np.float64) * scale
v0 = np.array([[0.0, 5.4], [0.0, 6.8], [0.0, 9.69], [0.0, 13.07]], dtype = np.float64) * pow(10, 3)

odeint_solver = OdeintSolver(t, m, N, c, M, r0, v0, iters_num)
R0 = odeint_solver.solve()
R0_ = np.array(R0)
#print(R0_.shape)

pure_python_verlet = PurePythonVerlet(t, m, N, c, M, r0, v0, iters_num)
R1 = pure_python_verlet.run()
R1_ = np.array(R1)
#print(R1_.shape)

error = 0
for i in range(len(R0)):
    for j in range(N):
        error += np.linalg.norm(R0[i][j] - R1[i][j])
print(error / scale)

print(np.linalg.norm(R0_ - R1_) / scale)
