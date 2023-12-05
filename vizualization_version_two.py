import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
from matplotlib.animation import FuncAnimation, PillowWriter

# Параметры веревки

# Параметры веревки
length = 0.5  # длина веревки
num_points = 50  # количество точек на веревке
time_steps = 50000  # количество временных шагов
# dt = 0.005  # шаг по времени
c = 50
M = 2
m = 0.1
# mass_array = np.array(
#     [1 + i * 1 / (num_points - 1) for i in range(num_points)][::-1])/60  # масса равномерно меняется от 1 до 10
mass_array = np.array([M - (M - m) / num_points * i for i in range(num_points)]) / 40
print(mass_array)
print(sum(mass_array))
g = 9.81

num_gu = 1  # количество точек закрепления
# tau = np.sqrt(m / c) / (2*np.pi)
tau = np.pi * np.sqrt(mass_array[0] / c)

# Начальные условия оси Ox

x_0 = np.linspace(0, length, num_points) / length

# Начальные условия оси Oy

# y_0 = np.sin(np.linspace(0, 2 * np.pi, num_points))
y_0 = np.zeros(num_points)  # изначально точки находятся на линии y = 0

# y_0[-1] = 1
y_0 = y_0 / length

x = x_0.copy()
y = y_0.copy()

# Нулевые начальные условия на скорость вдоль оси Ox

velocity_x = np.zeros(num_points) / length * tau

# Нулевые начальные условия на скорость вдоль оси Oy


# velocity_y = np.cos(np.linspace(0, 2 * np.pi, num_points))
velocity_y = np.zeros(num_points) / length * tau

F_x = np.zeros(num_points - num_gu)
F_y = np.zeros(num_points - num_gu)

print(len(F_x))

t = np.linspace(0, 50 * tau, time_steps) / tau

print(f'tau = {tau}')

dt = t[1] - t[0]
print(f'Шаг времени деленный на период = {dt / tau}')

x[0] = 0
y[0] = 0
velocity_x[0] = 0
velocity_y[0] = 0

# x[1] = x_0[1]
# y[1] = y_0[1]
# velocity_x[1] = 0
# velocity_y[1] = 0
#
# x[2] = x_0[2]
# y[2] = y_0[2]
# velocity_x[2] = 0
# velocity_y[2] = 0


# x[num_points - 1] = 1
# y[num_points - 1] = 0
# velocity_x[num_points - 1] = 0
# velocity_y[num_points - 1] = 0

a = 1 / num_points
coefficient = np.array([(mass_array[i] * g) / (c * length) for i in range(num_points)])
# print(coefficient)
print(0.5 * a)

# Создание графика
fig, ax = plt.subplots()
# plt.ylim(-100, 100)
plt.ylim(-10, 10)
line, = ax.plot(x, y, marker='o')

# надо в разных циклах искать скорости и перемещения
# Функция обновления графика на каждом временном шаге
flag = 1

frame_count = 500


def update(frame):
    # print(frame)
    global x, y, velocity_x, velocity_y, x, y, x_0, y_0, F_x, F_y, flag, frame_count

    delta_x = x[num_gu] - x[num_gu - 1]
    delta_y = y[num_gu] - y[num_gu - 1]
    l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)
    F_x[0] = (l1 - a) * delta_x / l1
    F_y[0] = (l1 - a) * delta_y / l1
    # velocity_x[0] = 0
    # velocity_y[0] = 0

    # if (frame == 1):
    #     velocity_y[0] = flag * 10
    #     flag = flag * (-1)
    # if (frame % 500 == 0) and (frame != 0):
    #     velocity_y[0] = flag * 10
    #     flag = flag * (-1)
    # if (frame == 1):
    #     velocity_y[num_points-1] = flag
    #     # flag = flag * (-1)

    # govnokod
    if (frame == 1):
        velocity_y[0] = flag * 5
        flag = flag * (-1)
    if (frame == frame_count) and (frame != 0) and (frame <= 4000):
        velocity_y[0] = flag * 5
        flag = flag * (-1)
        frame_count += 1000
    if (frame > 4000):
        velocity_y[0] = 0


    # velocity_x[0] = 0
    # velocity_y[0] = 0

    for j in range(1, num_points - 1):
        # print(i, j)

        delta_x = x[j + 1] - x[j]
        delta_y = y[j + 1] - y[j]
        l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)

        F_x[j] = (l1 - a) * delta_x / l1
        F_y[j] = (l1 - a) * delta_y / l1

        velocity_x[j] = velocity_x[j] + (F_x[j] - F_x[j - 1]) * dt * (4 * np.pi ** 2)
        velocity_y[j] = velocity_y[j] + (F_y[j] - F_y[j - 1] - coefficient[j]) * dt * (4 * np.pi ** 2)

    velocity_x[num_points - 1] = velocity_x[num_points - 1] + (-F_x[num_points - 1 - 1]) * dt * (4 * np.pi ** 2)
    velocity_y[num_points - 1] = velocity_y[num_points - 1] + (
            -F_y[num_points - 1 - 1] - coefficient[num_points - 1]) * dt * (4 * np.pi ** 2)

    for j in range(num_points):
        x[j] = x[j] + velocity_x[j] * dt
        y[j] = y[j] + velocity_y[j] * dt
        if (1<=j<=num_points-2) and (y[j] < y[j-1]):
            x[j] = max(x[j], x[j-1])



    if frame % 50 == 0:
        full_energy = 0
        for k in range(num_points):
            full_energy += 0.5 * c * (
                    (x[k] - x_0[k]) ** 2 + (y[k] - y_0[k]) ** 2) ** 0.5 + 0.5 * m * velocity_x[k] ** 2 + m * g * (
                                   y[k] - y_0[k])

        # print(f'Цикл № {frame}', 'Полная энергия = ', full_energy)
        print(f'Цикл № {frame}')
        line.set_ydata(y)
        line.set_xdata(x)
    return line,


# Создание анимации
ani = FuncAnimation(fig, update, frames=100000, interval=1, blit=True)

# Сохранение анимации в видеофайл GIF
# ani.save('animation_2.gif', writer='pillow', fps=40)

# ani.save("TLI.gif", dpi=300, writer=PillowWriter(fps=25))


# Отображение анимации
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Движение хлыста')
plt.show()
