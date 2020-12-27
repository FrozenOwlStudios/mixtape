import argparse
import numpy as np
import pandas as pd

PROGRAM_DESCRIPTION = 'This program is used for generation of signals (WRITE MORE)'

class Sinusoid:

    def __init__(self, amplitude, frequency, phase, offset):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.offset = offset

    def __str__(self):
        return f'A:{self.amplitude} F:{self.frequency} P:{self.phase} O:{self.offset}'


def parse_arguments():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    return parser.parse_args()

def main(args):
    sinusoid = Sinusoid(1.0, 10000.0, 0.0, 0.0)
    print(f'{sinusoid}')


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
