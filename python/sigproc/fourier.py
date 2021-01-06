import argparse
import numpy as np
import pandas as pd 


def caveman_approach(signal_file):
    signal = pd.read_csv(signal_file).to_numpy()
    complex_signal = np.apply_along_axis(lambda args: [complex(*args)], 3, signal)
    

def main(args):
    pass 


def parse_arguments():
    parser = argparse.ArgumentParser
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
