import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры веревки
length = 0.5  # длина веревки
num_points = 20  # количество точек на веревке
time_steps = 1000  # количество временных шагов
# dt = 0.005  # шаг по времени
c = 500
m = 10
g = 9.81
# tau = np.sqrt(m / c) / (2*np.pi)
tau = np.pi * np.sqrt(m / c)

# Начальные условия оси Ox
x_0 = np.linspace(0, length, num_points)
x_0 = x_0 / length
# Начальные условия оси Oy
# y_0 = np.sin(np.linspace(0, 2 * np.pi, num_points))
y_0 = np.ones(num_points)
# y_0[10] = - 5
y_0 = y_0 / length

x_last = x_0.copy()
y_last = y_0.copy()

x = x_0.copy()
y = y_0.copy()

# Нулевые начальные условия на скорость вдоль оси Ox
vel_x_last = np.zeros(num_points)
vel_x_last = vel_x_last / length * tau
# Нулевые начальные условия на скорость вдоль оси Oy
vel_y_last = np.zeros(num_points)
# vel_y_last[10] = 10
vel_y_last = vel_y_last / length * tau

vel_x = np.zeros(num_points)

vel_y = np.zeros(num_points)

F_x = np.zeros(num_points - 1)
F_y = np.zeros(num_points - 1)

t = np.linspace(0, 5 * tau, time_steps)
t = t / tau
print(f'tau = {tau}')

print(f'Шаг времени деленный на период = {t[1] / tau}')
dt = t[1] - t[0]

x[0] = 0
y[0] = 0
vel_x[0] = 0
vel_y[0] = 0

x[num_points - 1] = 1
y[num_points - 1] = 0
vel_x[num_points - 1] = 0
vel_y[num_points - 1] = 0

a = 1 / num_points
coefficient = (m * g) / (c * length)
# print(coefficient)
print(0.5 * a)

# Создание графика
fig, ax = plt.subplots()
plt.ylim(-100, 100)
line, = ax.plot(x, y, marker='o')


# надо в разных циклах искать скорости и перемещения
# Функция обновления графика на каждом временном шаге
def update(frame):
    # print(frame)
    global x, y, vel_x_last, vel_y_last, x_last, y_last, F_x, F_y

    for j in range(num_points):
        # print(i, j)
        if j == 0:
            delta_x = x[j + 1] - x[j]
            delta_y = y[j + 1] - y[j]
            l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)
            F_x[j] = (l1 - a) * delta_x / l1
            F_y[j] = (l1 - a) * delta_y / l1
            vel_x[j] = 0
            vel_y[j] = 0
            continue

        if j == num_points - 1:
            vel_x[j] = 0
            vel_y[j] = 0
            continue

        delta_x = x[j + 1] - x[j]
        delta_y = y[j + 1] - y[j]
        l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)

        F_x[j] = (l1 - a) * delta_x / l1
        F_y[j] = (l1 - a) * delta_y / l1

        vel_x[j] = vel_x_last[j] + (F_x[j] - F_x[j - 1]) * dt / (4 * np.pi ** 2)
        vel_y[j] = vel_y_last[j] + (F_y[j] - F_y[j - 1] - coefficient) * dt / (4 * np.pi ** 2)
        # print(vel_y[j])

    # print(f'Скорость Ox = {vel_x}')
    # print(f'Скорость Oy = {vel_y}')

    vel_x_last = vel_x.copy()
    vel_y_last = vel_y.copy()

    for j in range(num_points):
        # print(f'Скорость Ox = {vel_x[j]}')
        # if j == 0 or j == num_points-1:
        #     continue
        x[j] = x_last[j] + vel_x[j] * dt
        # print(x[j] - x[j-1])
        # if abs(x[j] - x[j - 1]) < 0.3 * a:
        #     if (x[j] - x[j - 1]) > 0:
        #         # x[j] = x_last[j] + 0.3 * a
        #         x[j] = 0.3 * a
        #     else:
        #         x[j] = - 0.3 * a
        #         # x[j] = x_last[j] - 0.3 * a
        # if abs(x[j] - x[j - 1]) > 1.5 * a:
        #     if (x[j] - x[j - 1]) > 0:
        #         # x[j] = x_last[j] + 1.5 * a
        #         x[j] = 1.5 * a
        #     else:
        #         x[j] = - 1.5 * a
        #         # x[j] = x_last[j] - 1.5 * a

        # print(f'x = {x[j]}')
        # print(f'Скорость Oy = {vel_y[j]}')
        y[j] = y_last[j] + vel_y[j] * dt

        # if abs(y[j] - y[j-1]) < 0.3*a:
        #     if (y[j] - y[j - 1]) > 0:
        #         # y[j] = y_last[j] + 0.3 * a
        #         y[j] = 0.3 * a
        #     else:
        #         # y[j] = y_last[j] - 0.3 * a
        #         y[j] = - 0.3 * a
        # if abs(y[j] - y[j-1]) > 1.5 * a:
        #     if (y[j] - y[j - 1]) > 0:
        #         # y[j] = y_last[j] + 1.5 * a
        #         y[j] = 1.5 * a
        #     else:
        #         y[j] = -1.5 * a
        #         # y[j] = y_last[j] - 1.5 * a

        # if (y[j] - y_last[j]) > 0.5*a:
        #     y[j] = y_last[j] + 0.5*a
        # print(f'y = {y[j]}')

    # print(f'x = {x}')
    # print(f'y = {y}')

    x_last = x.copy()
    y_last = y.copy()

    if frame % 10 == 0:
        Energia = sum(0.5 * m * vel_x_last ** 2 + 0.5 * c * ((x - x_last) ** 2 + (y - y_last) ** 2) + m * g * y)
        print(f'Цикл № {frame}', 'Полная энергия = ', Energia)
        line.set_ydata(y)
        line.set_xdata(x)
    return line,


# Создание анимации
ani = FuncAnimation(fig, update, frames=1000000, interval=1, blit=True)

# Отображение анимации
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Гибкие движения веревки')
plt.show()
