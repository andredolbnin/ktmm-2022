import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.animation as anime

from OdeintSolver import OdeintSolver
from PurePythonVerlet import PurePythonVerlet

t = pow(10, 7) * 1.5
scale = pow(10, 12)
iters_num = pow(10, 3)

w = 5 * scale
h = 5 * scale

c = np.array([0.0, 0.0])

m = np.array([1.0243, 0.87, 5.68, 18.986], dtype = np.float64) * pow(10, 26)
M = 1.9 * pow(10, 30)

N = 4

r0 = np.array([[4.5, 0.0], [2.8, 0.0], [1.43, 0.0], [0.8, 0.0]], dtype = np.float64) * scale
v0 = np.array([[0.0, 5.4], [0.0, 6.8], [0.0, 9.69], [0.0, 13.07]], dtype = np.float64) * pow(10, 3) # км -> м

solver = PurePythonVerlet(t, m, N, c, M, r0, v0, iters_num)
R = solver.run()
#odeint_solver = OdeintSolver(t, m, N, c, M, r0, v0, iters_num)
#R = odeint_solver.solve()


fig = plt.figure()
ax = plt.axes(xlim=(-w, w + scale), ylim=(-h, h))
ax.set_facecolor((0, 0, 0.1))
plt.xlabel("x (млрд. км.)")
plt.ylabel("y (млрд. км.)")
plt.title("Планеты-гиганты Солнечной системы")
plt.style.use("dark_background")

neptune_color = "blue"
uranus_color = (0.16, 0.5, 0.5)
saturn_color = (0.75, 0.78, 0.22)
jupiter_color = (0.964, 0.4, 0.2)
sun_color = "yellow"
lw = 4
legend_elements = [lines.Line2D([0], [0], color = neptune_color, lw = lw),
                   lines.Line2D([0], [0], color = uranus_color, lw = lw),
                   lines.Line2D([0], [0], color = saturn_color, lw = lw),
                   lines.Line2D([0], [0], color = jupiter_color, lw = lw),
                   lines.Line2D([0], [0], color = sun_color, lw = lw)]

ax.legend(legend_elements, ["Нептун",
                            "Уран",
                            "Сатурн",
                            "Юпитер",
                            "Солнце"])

sun = plt.Circle(c, 0.3 * scale, fc = sun_color)
ax.add_patch(sun)

neptune = plt.Circle((4.5 * scale, 0.0), 0.1 * scale, fc = neptune_color)
uranus = plt.Circle((2.8 * scale, 0.0), 0.1 * scale, fc = uranus_color)
saturn = plt.Circle((1.43 * scale, 0.0), 0.15 * scale, fc = saturn_color)
jupiter = plt.Circle((0.8 * scale, 0.0), 0.2 * scale, fc = jupiter_color)
planets = []

def init():
    neptune.center = (4.5 * scale, 0.0)
    uranus.center = (2.8 * scale, 0.0)
    saturn.center = (1.43 * scale, 0.0)
    jupiter.center = (0.8 * scale, 0.0)
    ax.add_patch(neptune)
    ax.add_patch(uranus)
    ax.add_patch(saturn)
    ax.add_patch(jupiter)
    planets.append(neptune)
    planets.append(uranus)
    planets.append(saturn)
    planets.append(jupiter)
    return planets

def animate(i):
    j = i % iters_num # зацикливаем
    if j >= iters_num: SystemExit()
    for k in range(N):
        planets[k].center = R[j][k]
    return planets


anim = anime.FuncAnimation(fig,
                           animate,
                           init_func=init,
                           frames=360,
                           interval=20,
                           blit=True)
