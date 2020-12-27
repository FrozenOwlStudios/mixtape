import argparse
import numpy as np
import pandas as pd

PROGRAM_DESCRIPTION = 'This program is used for generation of signals (WRITE MORE)'

def generate_sampling(start_timestamp, end_timestamp, sampling_frequency):
    sample_count = (end_timestamp - start_timestamp) * sampling_frequency
    return np.linspace(start_timestamp, end_timestamp, sample_count)


def randomize(lims):
    return np.random.uniform(lims[0], lims[1])


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


def parse_arguments():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    return parser.parse_args()


def main(args):
    sinusoid = Sinusoid.generate_random([1.0, 10.0], [1.0, 10000.0], [0.0, 3.0], [0.0, 2.0])
    print(f'{sinusoid}')


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
