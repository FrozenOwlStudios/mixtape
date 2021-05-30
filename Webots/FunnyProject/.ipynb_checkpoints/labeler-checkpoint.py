'''
This is script for labelling data for FunnyProject.
'''

import argparse
import os
import cv2
import tensorflow as tf
import numpy as np

LEFT = ord('a')
RIGHT = ord('d')
FORWARD = ord('w')
REVERSE = ord('s')


target_counts = {
        LEFT : 0,
        RIGHT : 0,
        FORWARD : 0,
        REVERSE : 0
        }

target_paths = None

def save_image(category, image):
    global target_counts
    path = target_paths[category]
    target_file = f'{path}/{target_counts[category]}.png'
    print(f'Target file -> {target_file}')
    cv2.imwrite(target_file, image)
    target_counts[category] += 1

def aug_noise(category, image, count):
    for _ in range(count):
        noise = np.random.normal(0.0, 0.05, size=image.shape)*255
        noised_image = image + noise
        save_image(category, noised_image)

def aug_flipped(category, image, count):
    if category == RIGHT:
        category = LEFT
    elif category == LEFT:
        category = RIGHT 
    flipped_image = cv2.flip(image, 1)
    save_image(category, flipped_image)
    aug_noise(category, flipped_image, count)

def main(args):
    global target_paths
    input_path = args.input_folder
    target_paths = {
            LEFT: f'{args.output_folder}/left',
            RIGHT: f'{args.output_folder}/right',
            FORWARD: f'{args.output_folder}/forward',
            REVERSE: f'{args.output_folder}/reverse'
            }



    for filename in os.listdir(input_path):
        if filename.endswith('.png'):
            img = cv2.imread(f'{input_path}/{filename}')
            resized_img = cv2.resize(img, (0,0), fx=3, fy=3)
            cv2.imshow('Image', resized_img)
            choice = cv2.waitKey(0)
            save_image(choice, img)
            aug_noise(choice, img, 3)
            aug_flipped(choice, img, 3)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', default='screenshots')
    parser.add_argument('-o', '--output_folder', default='dataset')
    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
