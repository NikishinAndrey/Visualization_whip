import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры веревки

# Параметры веревки
length = 0.5  # длина веревки
num_points = 40  # количество точек на веревке
time_steps = 1000  # количество временных шагов
# dt = 0.005  # шаг по времени
c = 500
m = 10
mass_array = np.array([1+ i*9/(num_points-1) for i in range(num_points)][::-1]) # масса равномерно меняется от 1 до 10
print(mass_array)
g = 9.81
# tau = np.sqrt(m / c) / (2*np.pi)
tau = np.pi * np.sqrt(m / c)

# Начальные условия оси Ox

x_0 = np.linspace(0, length, num_points) / length

# Начальные условия оси Oy

y_0 = np.sin(np.linspace(0, 2 * np.pi, num_points))
# y_0 = np.zeros(num_points)  # изначально точки находятся на линии y = 0

# y_0[-1] = 1
y_0 = y_0 / length

x = x_0.copy()
y = y_0.copy()

# Нулевые начальные условия на скорость вдоль оси Ox

velocity_x = np.zeros(num_points) / length * tau

# Нулевые начальные условия на скорость вдоль оси Oy


velocity_y = np.cos(np.linspace(0, 2 * np.pi, num_points))

F_x = np.zeros(num_points - 1)
F_y = np.zeros(num_points - 1)

t = np.linspace(0, 50 * tau, time_steps) / tau

print(f'tau = {tau}')

print(f'Шаг времени деленный на период = {t[1] / tau}')
dt = t[1] - t[0]

x[0] = 0
y[0] = 0
velocity_x[0] = 0
velocity_y[0] = 0

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
plt.ylim(-100, 100)
line, = ax.plot(x, y, marker='o')


# надо в разных циклах искать скорости и перемещения
# Функция обновления графика на каждом временном шаге
def update(frame):
    # print(frame)
    global x, y, velocity_x, velocity_y, x, y, x_0, y_0, F_x, F_y

    delta_x = x[1] - x[0]
    delta_y = y[1] - y[0]
    l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)
    F_x[0] = (l1 - a) * delta_x / l1
    F_y[0] = (l1 - a) * delta_y / l1
    velocity_x[0] = 0
    velocity_y[0] = 0

    # velocity_x[num_points - 1] = 0
    # velocity_y[num_points - 1] = 0

    for j in range(1, num_points):
        # print(i, j)

        if j == num_points - 1:
            velocity_x[j] = velocity_x[j] + (-F_x[j - 1]) * dt / (4 * np.pi ** 2)
            velocity_y[j] = velocity_y[j] + (-F_y[j - 1] - coefficient[j]) * dt / (4 * np.pi ** 2)
            continue

        delta_x = x[j + 1] - x[j]
        delta_y = y[j + 1] - y[j]
        l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)

        F_x[j] = (l1 - a) * delta_x / l1
        F_y[j] = (l1 - a) * delta_y / l1

        velocity_x[j] = velocity_x[j] + (F_x[j] - F_x[j - 1]) * dt / (4 * np.pi ** 2)
        velocity_y[j] = velocity_y[j] + (F_y[j] - F_y[j - 1] - coefficient[j]) * dt / (4 * np.pi ** 2)

    for j in range(num_points):
        x[j] = x[j] + velocity_x[j] * dt
        y[j] = y[j] + velocity_y[j] * dt

    if frame % 10 == 0:
        full_energy = 0
        for k in range(num_points):
            full_energy += 0.5 * c * (
                    (x[k] - x_0[k]) ** 2 + (y[k] - y_0[k]) ** 2) ** 0.5 + 0.5 * m * velocity_x[k] ** 2 + m * g * (
                                       y[k] - y_0[k])

        print(f'Цикл № {frame}', 'Полная энергия = ', full_energy)
        line.set_ydata(y)
        line.set_xdata(x)
    return line,


# Создание анимации
ani = FuncAnimation(fig, update, frames=1000000, interval=1, blit=True)

# Отображение анимации
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Движение хлыста')
plt.show()
