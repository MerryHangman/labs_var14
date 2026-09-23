"""Чтение wav-файла и приведение сигнала к удобному для анализа виду."""

import numpy as np
from scipy.io import wavfile


def read_wav(path):
    """Читает wav-файл и возвращает частоту дискретизации и отсчёты.

    Работает с mono и stereo файлами, а также с int16/int32/float wav.
    При stereo сигнал усредняется по каналам, чтобы дальнейший анализ
    (спектр, осциллограмма, гистограмма) выполнялся по одной дорожке.

    Возвращает:
        sampling_rate (int) - частота дискретизации, Гц.
        samples (np.ndarray[float64]) - отсчёты сигнала.
    """
    sampling_rate, raw_samples = wavfile.read(path)

    # Приводим к float64, чтобы не потерять точность при усреднении
    # каналов и не переполнить целочисленный тип при возведении в квадрат.
    samples = raw_samples.astype(np.float64)

    if samples.ndim == 2:
        # Stereo и более: усредняем все каналы в один.
        samples = samples.mean(axis=1)

    return sampling_rate, samples
