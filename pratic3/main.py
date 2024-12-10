import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from IPython.display import clear_output
import random
import time


def create_grid(n, blue_ratio=0.45, red_ratio=0.45, empty_ratio=0.1):
    """Создаем начальную сетку с заданным процентным соотношением клеток."""
    cells = [1] * int(blue_ratio * n * n) + [2] * int(red_ratio * n * n) + [0] * int(empty_ratio * n * n)
    np.random.shuffle(cells)
    grid = np.array(cells).reshape(n, n)
    return grid


def is_happy(grid, x, y):
    """Проверяем, счастлива ли клетка (имеет ли >= 2 соседей того же цвета)."""
    color = grid[x, y]
    if color == 0:
        return True  # Пустые клетки всегда "счастливы"

    # Получаем соседей клетки
    neighbors = grid[max(0, x - 1):min(grid.shape[0], x + 2), max(0, y - 1):min(grid.shape[1], y + 2)]
    same_color_neighbors = np.sum(neighbors == color) - 1  # Не учитывать саму клетку
    return same_color_neighbors >= 2


def find_unhappy_cells(grid):
    """Находим все несчастливые клетки."""
    unhappy_cells = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] != 0 and not is_happy(grid, x, y):
                unhappy_cells.append((x, y))
    return unhappy_cells


def simulate_step(grid):
    """Производим один шаг симуляции: перемещаем одну случайную несчастливую клетку в пустую ячейку."""
    unhappy_cells = find_unhappy_cells(grid)
    if not unhappy_cells:
        return False  # Если нет несчастливых клеток, симуляция завершена

    # Выбираем случайную несчастливую клетку и перемещаем её в случайную пустую ячейку
    x, y = random.choice(unhappy_cells)
    empty_cells = list(zip(*np.where(grid == 0)))
    new_x, new_y = random.choice(empty_cells)

    # Перемещаем клетку
    grid[new_x, new_y] = grid[x, y]
    grid[x, y] = 0
    return True


def run_simulation(n, steps, delay):
    """Запускаем симуляцию и обновляем визуализацию сетки в Jupyter Notebook."""
    grid = create_grid(n)
    cmap = ListedColormap(['white', 'blue', 'red'])
    for step in range(steps):
        clear_output(wait=True)  # Очищаем вывод
        plt.imshow(grid, cmap=cmap, interpolation='nearest')
        plt.title(f'Step {step + 1}')
        plt.show()
        time.sleep(delay)  # Задержка для лучшего отображения

        # Выполняем шаг симуляции
        if not simulate_step(grid):
            print("Стабилизация достигнута на шаге", step + 1)
            break


# Параметры модели
n = 50  # Размер сетки
steps = 100000  # Количество шагов
delay = 0.001  # Задержка между шагами для анимации

run_simulation(n, steps, delay)
