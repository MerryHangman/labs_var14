"""Спектральный анализ сигнала.

Вариант 14: тип спектрального анализа - квадрат ДПФ, Re**2 + Im**2.
"""

import numpy as np


def power_spectrum(samples, sampling_rate):
    """Считает квадрат ДПФ (Re**2 + Im**2) по всем отсчётам сигнала.

    Так как исходный сигнал вещественный, спектр симметричен
    относительно частоты Найквиста, поэтому для наглядности графика
    возвращается только "полезная" половина: от 0 до fs/2.

    Возвращает:
        freqs (np.ndarray) - ось частот, Гц.
        power (np.ndarray) - значения Re**2 + Im**2 для каждой частоты.
    """
    spectrum = np.fft.fft(samples)

    real_part = spectrum.real
    imag_part = spectrum.imag
    power = real_part ** 2 + imag_part ** 2

    freqs = np.fft.fftfreq(len(samples), d=1.0 / sampling_rate)

    # Оставляем только неотрицательные частоты (0 .. fs/2)
    half = len(samples) // 2
    return freqs[:half], power[:half]
