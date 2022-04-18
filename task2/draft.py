# черновой скрипт для реализации алгоритма Верле и визуализации

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.animation as anime

t = pow(10, 7) * 1.5
scale = pow(10, 12)
iters_num = pow(10, 3) # время и количетсво итераций такие, что Нептун проходит один круг

w = 5 * scale # 5, чтобы 4.5 расстояния до Нептуна хватало
h = 5 * scale

c = np.array([0.0, 0.0]) # координаты Солнца и центр

G = 6.6743 * pow(10, -11)

# массы планет (Нептун, Уран, Сатурн, Юпитер)
m = np.array([1.0243, 0.87, 5.68, 18.986], dtype = np.float64) * pow(10, 26)
M = 1.9 * pow(10, 30) # масса Солнца

N = 4 # количество планет

def acceleration(r):
    a = []
    for i in range(N):
        tmp = 0
        for j in range(N):
            if i == j: continue
            tmp += G * m[j] * (r[j] - r[i]) / np.linalg.norm(r[j] - r[i]) ** 3
        tmp += G * M * (c - r[i]) / np.linalg.norm(c - r[i]) ** 3
        a.append(tmp)
    return np.array(a, dtype = np.float64)

def next_r(r, v, a):
    return r + v * t + 0.5 * a * t * t

def next_v(v, a, next_a):
    return v + 0.5 * (a + next_a) * t

# расстояния и скорости планет в случае парада планет справа от Солнца
r0 = np.array([[4.5, 0.0], [2.8, 0.0], [1.43, 0.0], [0.8, 0.0]], dtype = np.float64) * scale
v0 = np.array([[0.0, 5.4], [0.0, 6.8], [0.0, 9.69], [0.0, 13.07]], dtype = np.float64) * pow(10, 3) # км -> м

R = np.zeros((iters_num, N, 2), dtype = np.float64)
V = np.zeros((iters_num, N, 2), dtype = np.float64)
A = np.zeros((iters_num, N, 2), dtype = np.float64)

R[0] = r0
V[0] = v0
A[0] = acceleration(r0)

for i in range(iters_num - 1):
    # Velocity Verlet
    R[i + 1] = next_r(R[i], V[i], A[i])
    A[i + 1] = acceleration(R[i + 1])
    V[i + 1] = next_v(V[i], A[i], A[i + 1])


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
