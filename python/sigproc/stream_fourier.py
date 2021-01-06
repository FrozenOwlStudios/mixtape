import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def quickplot(x, y, title):
    plt.title(title)
    plt.plot(x,y)
    plt.show()


def fourier(time, amplitude_in_time, frequency_steps):
    frequencies = []
    amplitude_in_frequency = []
    n = len(time)
    for k in range(n):
        frequency_sum = 0.0
        amplitude_sum = 0.0
        for t in range(n):
            phi = 2 * np.pi * t * k / n
            frequency_sum += time[t]*np.cos(phi) + amplitude_in_time[t]*np.sin(phi)
            amplitude_sum += -time[t]*np.sin(phi) + amplitude_in_time[t]*np.cos(phi)
        frequencies.append(frequency_sum)
        amplitude_in_frequency.append(amplitude_sum)
    return np.asarray(frequencies), np.asarray(amplitude_in_frequency)



def main(args):
    data = pd.read_csv(args.input_file)
    print(data.head())
    time = data['timestamp'].to_numpy()
    amplitude_in_time = data['signal'].to_numpy()
    quickplot(time, amplitude_in_time, 'Input signal')
    placeholder = np.zeros(len(amplitude_in_time))
    frequencies, amplitude_in_frequency = fourier(amplitude_in_time, placeholder, args.frequency_steps)
    plt.plot(frequencies)
    plt.show()
    plt.plot(amplitude_in_frequency)
    plt.show()
    quickplot(frequencies, amplitude_in_frequency, 'Frequency spectrum')
    spectrum = pd.DataFrame({'frequency':frequencies, 'amplitude':amplitude_in_frequency})
    spectrum.to_csv('debug.csv')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Implementacja transformacji Fouriera')
    parser.add_argument('-i', '--input_file', type=str, required=True,
            help='Csv file with time series')
    parser.add_argument('-s', '--frequency_steps', type=int, default=30,
            help='')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
