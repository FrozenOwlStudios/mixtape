import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROGRAM_DESCRIPTION = 'This program is used for generation of signals (WRITE MORE)'

def generate_sampling(start_timestamp, end_timestamp, sampling_frequency):
    sample_count = (end_timestamp - start_timestamp) * sampling_frequency
    return np.linspace(start_timestamp, end_timestamp, sample_count)


def randomize(lims):
    return np.random.uniform(lims[0], lims[1])

def parse_range(range_str):
    lower, upper = map(float, range_str.split(','))
    return (lower, upper)

class Sinusoid:

    def __init__(self, amplitude, frequency, phase, offset):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.offset = offset

    def generate_signal(self, sampling):
        return (self.amplitude * np.sin( 2*np.pi*self.frequency*sampling + self.phase) \
                + self.offset)

    def __str__(self):
        return f'A:{self.amplitude} F:{self.frequency} P:{self.phase} O:{self.offset}'

    @staticmethod
    def generate_random(amplitude, frequency, phase, offset):
        return Sinusoid(randomize(amplitude), randomize(frequency), randomize(phase),
                randomize(offset))

class SignalGenerator:

    def __init__(self):
        self.sinusoids = []

    def __getitem__(self, index):
        return self.sinusoids[index]

    def append(self, sinusoid):
        self.sinusoids.append(sinusoid)

    def generate_signal(self, sampling):
        signal = self.sinusoids[0].generate_signal(sampling)
        for sinusoid in self.sinusoids[1:]:
            signal += sinusoid.generate_signal(sampling)
        return signal

    @staticmethod
    def generate_random(sinusoid_count, amplitude, frequency, phase, offset):
        generator = SignalGenerator()
        for _ in range(sinusoid_count):
            generator.append(Sinusoid.generate_random(amplitude, frequency, phase, offset))
        return generator

def parse_arguments():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('-c', '--csv_file',
            default=None, help='File to which signal data will be saved')
    parser.add_argument('-s', '--sin_count', default=1, type=int,
            help='Number of sinusoids')
    parser.add_argument('-a', '--amplitude', default=(1,10), type=parse_range,
            help='Number of sinusoids')
    parser.add_argument('-f', '--frequency', default=(1,1000), type=parse_range,
            help='Number of sinusoids')
    parser.add_argument('-p', '--phase', default=(0,0), type=parse_range,
            help='Number of sinusoids')
    parser.add_argument('-o', '--offset', default=(0,0), type=parse_range,
            help='Number of sinusoids')
    return parser.parse_args()


def main(args):
    sinusoid = SignalGenerator.generate_random(args.sin_count, args.amplitude,
            args.frequency, args.phase, args.offset)
    print(f'{sinusoid}')
    sampling = generate_sampling(0,10,100)
    signal = sinusoid.generate_signal(sampling)
    plt.plot(sampling, signal)
    plt.show()
    if args.csv_file is not None:
        data = {'timestamp':sampling, 'signal':signal}
        data = pd.DataFrame(data)
        data.to_csv(args.csv_file, index=False)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
