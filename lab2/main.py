"""Лабораторная работа №2. Вариант 14.

Визуализация и спектральный анализ речевых сигналов с Python.

Вариант 14:
    - тип графика для отсчётов сигнала: столбчатая диаграмма;
    - тип спектрального анализа: квадрат ДПФ (Re**2 + Im**2);
    - частота дискретизации wav-файла: 11025 Гц.

Строит 4 графика:
    1. Столбчатая диаграмма N отсчётов сигнала (N вводится с клавиатуры).
    2. Осциллограмма сигнала как функция времени.
    3. Квадрат ДПФ в зависимости от частоты.
    4. Гистограмма амплитудных значений отсчётов.
"""

import time

# Импорт работает и при запуске "python lab2/main.py" напрямую (тогда
# папка lab2 сама является корнем для импорта), и при запуске через
# общее меню labs_var14/main.py (тогда lab2 - это пакет).
try:
    from lab2 import plots, ui
    from lab2.spectrum import power_spectrum
    from lab2.wav_io import read_wav
except ImportError:
    import plots
    import ui
    from spectrum import power_spectrum
    from wav_io import read_wav

# Ожидаемая для варианта 14 частота дискретизации.
EXPECTED_SAMPLING_RATE = 11025


def describe_wav(path, sampling_rate, samples):
    """Печатает краткую информацию о загруженном wav-файле."""
    duration = len(samples) / sampling_rate
    print(f"\nФайл: {path}")
    print(f"Частота дискретизации: {sampling_rate} Гц")
    print(f"Количество отсчётов: {len(samples)}")
    print(f"Длительность записи: {duration:.2f} сек")

    if sampling_rate != EXPECTED_SAMPLING_RATE:
        print(
            f"Внимание: для варианта 14 ожидалась частота "
            f"{EXPECTED_SAMPLING_RATE} Гц, у файла - {sampling_rate} Гц. "
            f"Графики будут построены по реальной частоте файла."
        )


def main():
    """Точка входа лабораторной работы №2."""
    start_time = time.time()

    print("=" * 60)
    print("Лабораторная №2. Спектральный анализ речевого сигнала")
    print("Вариант 14: столбчатая диаграмма, квадрат ДПФ, 11025 Гц")
    print("=" * 60)

    path = ui.ask_wav_path()
    if path is None:
        print("Ввод прерван.")
        return

    try:
        sampling_rate, samples = read_wav(path)
    except Exception as error:
        # Программа не должна падать на "чужих" wav-файлах.
        print(f"Не удалось прочитать wav-файл: {error}")
        return

    if len(samples) == 0:
        print("Файл не содержит отсчётов сигнала.")
        return

    describe_wav(path, sampling_rate, samples)

    count = ui.ask_sample_count(max_value=len(samples))
    if count is None:
        print("Ввод прерван.")
        return

    freqs, power = power_spectrum(samples, sampling_rate)

    plots.plot_samples_bar(samples, count)
    plots.plot_oscillogram(samples, sampling_rate)
    plots.plot_power_spectrum(freqs, power)
    plots.plot_histogram(samples)

    print("\nОткрываются окна с графиками. Закройте их, чтобы завершить.")

    # Проверка на защите: время вычисления программы.
    print(time.time() - start_time, "seconds")

    plots.show_all()


if __name__ == "__main__":
    main()
