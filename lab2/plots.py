"""Построение четырёх графиков, требуемых заданием лабы 2 (вариант 14)."""

import numpy as np
import matplotlib.pyplot as plt


def plot_samples_bar(samples, count):
    """1) Столбчатая диаграмма первых `count` отсчётов сигнала.

    Тип графика для варианта 14 - столбчатая диаграмма.
    """
    x = np.arange(count)
    y = samples[:count]

    plt.figure("1. Чтение отсчётов сигнала")
    plt.bar(x, y, width=1.0)
    plt.xlabel("Номер отсчёта")
    plt.ylabel("Амплитуда")
    plt.title(f"Столбчатая диаграмма первых {count} отсчётов сигнала")
    plt.grid(axis="y", alpha=0.3)


def plot_oscillogram(samples, sampling_rate):
    """2) Осциллограмма сигнала как функция времени."""
    time_axis = np.arange(len(samples)) / sampling_rate

    plt.figure("2. Осциллограмма")
    plt.plot(time_axis, samples, linewidth=0.8)
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title("Осциллограмма звукового сигнала")
    plt.grid(alpha=0.3)


def plot_power_spectrum(freqs, power):
    """3) Квадрат ДПФ (Re**2 + Im**2) в зависимости от частоты."""
    plt.figure("3. Спектральный анализ")
    plt.plot(freqs, power, linewidth=0.8, color="darkorange")
    plt.xlabel("Частота, Гц")
    plt.ylabel("Re^2 + Im^2 (квадрат ДПФ)")
    plt.title("Спектральный анализ сигнала (квадрат ДПФ)")
    plt.grid(alpha=0.3)


def plot_histogram(samples):
    """4) Гистограмма амплитудных значений отсчётов сигнала."""
    plt.figure("4. Гистограмма")
    plt.hist(samples, bins=50, color="skyblue", edgecolor="black")
    plt.xlabel("Амплитуда")
    plt.ylabel("Количество отсчётов")
    plt.title("Гистограмма амплитуд сигнала")
    plt.grid(axis="y", alpha=0.3)


def show_all():
    """Показывает все построенные окна с графиками одновременно."""
    plt.show()
