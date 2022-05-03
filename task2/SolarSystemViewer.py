import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.animation as anime

from PurePythonVerlet import PurePythonVerlet
from MultiprocessingVerlet import MultiprocessingVerlet
from OpenClVerlet import OpenClVerlet
from CythonVerlet import CythonVerlet
from OdeintSolver import OdeintSolver


if __name__ == "__main__":
    t = pow(10, 5)
    scale = pow(10, 12)
    iters_num = 100
    
    w = 1 * scale
    h = 1 * scale
    
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
    
    ###############################################################################
    
    solver = PurePythonVerlet(t, m, N, c, M, r0, v0, iters_num)
    R = solver.run()
    
    #solver = MultiprocessingVerlet(t, m, N, c, M, r0, v0, iters_num)
    #R = solver.run()
    
    #solver = OpenClVerlet(t, m, N, c, M, r0, v0, iters_num)
    #R = solver.run()
    
    #solver = CythonVerlet(t, N, M, iters_num)
    #R = solver.run(m, c, r0, v0)
            
    #odeint_solver = OdeintSolver(t, m, N, c, M, r0, v0, iters_num)
    #R = odeint_solver.solve()
    
    #raise SystemExit()
    
    ###############################################################################
    
    fig = plt.figure()
    ax = plt.axes(xlim=(-w, w + 0.5 * scale), ylim=(-h, h))
    ax.set_facecolor((0, 0, 0.1))
    ax.set_xticks([-0.8 * scale, - 0.4 * scale, 0, 0.4 * scale, 0.8 * scale])
    ax.set_xticklabels([-28, -4, 0, 4, 28])
    ax.set_yticks([- 0.4 * scale, 0, 0.4 * scale])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Солнечная система")
    plt.style.use("dark_background")
    
    neptune_color = "blue"
    uranus_color = (0.16, 0.5, 0.5)
    saturn_color = (0.75, 0.78, 0.22)
    jupiter_color = (0.964, 0.4, 0.2)
    mars_color = "red"
    earth_color = (0.325, 0.533, 0.917)
    venus_color = "white"
    mercury_color = "gray"
    sun_color = "yellow"
    lw = 4
    legend_elements = [lines.Line2D([0], [0], color = neptune_color, lw = lw),
                       lines.Line2D([0], [0], color = uranus_color, lw = lw),
                       lines.Line2D([0], [0], color = saturn_color, lw = lw),
                       lines.Line2D([0], [0], color = jupiter_color, lw = lw),
                       lines.Line2D([0], [0], color = mars_color, lw = lw),
                       lines.Line2D([0], [0], color = earth_color, lw = lw),
                       lines.Line2D([0], [0], color = venus_color, lw = lw),
                       lines.Line2D([0], [0], color = mercury_color, lw = lw),
                       lines.Line2D([0], [0], color = sun_color, lw = lw)]
    
    ax.legend(legend_elements, ["Нептун",
                                "Уран",
                                "Сатурн",
                                "Юпитер",
                                "Марс",
                                "Земля",
                                "Венера",
                                "Меркурий",
                                "Солнце"],
              bbox_to_anchor = (1.1, 1.1))
    
    sun = plt.Circle(c, 0.025 * scale, fc = sun_color)
    ax.add_patch(sun)
    
    neptune_c = (4.5 * scale, 0.0)
    uranus_c = (2.8 * scale, 0.0)
    saturn_c = (1.43 * scale, 0.0)
    jupiter_c = (0.8 * scale, 0.0)
    mars_c = (0.23 * scale, 0.0)
    earth_c = (0.15 * scale, 0.0)
    venus_c = (0.11 * scale, 0.0)
    mercury_c = (0.057 * scale, 0.0)
    
    neptune = plt.Circle(neptune_c, 0.018 * scale, fc = neptune_color)
    uranus = plt.Circle(uranus_c, 0.018 * scale, fc = uranus_color)
    saturn = plt.Circle(saturn_c, 0.02 * scale, fc = saturn_color)
    jupiter = plt.Circle(jupiter_c, 0.022 * scale, fc = jupiter_color)
    mars = plt.Circle(mars_c, 0.012 * scale, fc = mars_color)
    earth = plt.Circle(earth_c, 0.012 * scale, fc = earth_color)
    venus = plt.Circle(venus_c, 0.012 * scale, fc = venus_color)
    mercury = plt.Circle(mercury_c, 0.008 * scale, fc = mercury_color)
    planets = []
    
    def init():
        neptune.center = neptune_c
        uranus.center = uranus_c
        saturn.center = saturn_c
        jupiter.center = jupiter_c
        mars.center = mars_c
        earth.center = earth_c
        venus.center = venus_c
        mercury.center = mercury_c
    
        ax.add_patch(neptune)
        ax.add_patch(uranus)
        ax.add_patch(saturn)
        ax.add_patch(jupiter)
        ax.add_patch(mars)
        ax.add_patch(earth)
        ax.add_patch(venus)
        ax.add_patch(mercury)
    
        planets.append(neptune)
        planets.append(uranus)
        planets.append(saturn)
        planets.append(jupiter)
        planets.append(mars)
        planets.append(earth)
        planets.append(venus)
        planets.append(mercury)
    
        return planets
    
    def animate(i):
        j = i % iters_num
        if j >= iters_num: SystemExit()
        for k in range(N):
            x = R[j][k][0]
            y = R[j][k][1]
            if np.sqrt(x ** 2 + y ** 2) > 0.4 * scale:
                x = np.sign(x) * pow(np.abs(x), 0.8) * pow(10, 3.1)
                y = np.sign(y) * pow(np.abs(y), 0.8) * pow(10, 3.1)
            if np.sqrt(x ** 2 + y ** 2) > 2.0 * scale:
                x = np.sign(x) * pow(np.abs(x), 0.6) * pow(10, 4.1)
                y = np.sign(y) * pow(np.abs(y), 0.6) * pow(10, 4.1)
            planets[k].center = (x, y)
            #planets[k].center = R[j][k]
        return planets
    
    
    anim = anime.FuncAnimation(fig,
                               animate,
                               init_func=init,
                               frames=360,
                               interval=20,
                               blit=True)
