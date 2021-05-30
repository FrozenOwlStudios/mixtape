'''This is a training script for the CNN. It takes the training data, trains a convolutional
neural network and saves it in the desired directory.'''

import os
import cv2
import glob
import pathlib
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.utils.np_utils import to_categorical
import tensorflow as tf
import numpy as np
import argparse

LABEL_TO_INT = {
    'W': 0,
    'A': 1,
    'D': 2,
    'E': 3,
    'S': 4,
}

def main(args):
    '''This is a main training script'''

    if args.data_dir != None:
        DATA_DIR = args.data_dir
    else:
        Exception("Data directory wasn't specified")

    if args.output_dir != None:
        save_model_path = f"{args.output_dir}/my_model.h5"
        save_model_architecture_path = f"{args.output_dir}/model.json"
        save_model_weights_path = f"{args.output_dir}/my_model_weights.h5"
    else:
        Exception("Output directory wasn't specified")

    images, labels, label_names = load_data(DATA_DIR)
    #print(f'Labels = {labels}')
    #labels = to_categorical(labels)
    images_train, images_test, labels_train, labels_test = train_test_split(images, labels, test_size=0.1)
    model = compose_model()
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    history = model.fit(images_train,
                        labels_train,
                        batch_size=64,
                        epochs=500,
                        validation_data=(images_train, labels_train),
                        validation_batch_size=256,
                        callbacks=[early_stopping])

    loss_and_accuracy = model.evaluate(images_test, labels_test, verbose=2)
    print_evaluation(loss_and_accuracy)

    save_model(model, save_model_path, save_model_architecture_path, save_model_weights_path)

def load_data(data_dir):
    '''This function loads all the data. It converts the photos to numpy arrays
    and prepares labels for the training'''

    
    categories = os.listdir(data_dir)
    category_count = len(categories)

    X = []
    Y = []

    for category_id, category in enumerate(categories):
        data_points = os.listdir(os.path.join(data_dir,category))
        for data_point in data_points: 
            if data_point.endswith('.png'):
                x = cv2.imread(os.path.join(data_dir,category,data_point))
                X.append(x)
                y = np.zeros(category_count)
                y[category_id] = 1
                Y.append(y)

    return np.array(X), np.array(Y), categories


def compose_model():
    '''This function composes a convolution neural network model'''

    model = Sequential()
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(100, 150, 3)))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(16, (3, 3), padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(16, (3, 3), padding='same'))
    model.add(Conv2D(8, (3, 3), padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(4, activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

    model.summary()

    return model

def print_evaluation(loss_and_accuracy):
    '''This function prints the evaluation of the model based on the given data'''

    print(f"Test loss: {loss_and_accuracy[0]}")
    print(f"Test accuracy: {loss_and_accuracy[1]}")

def save_model(model, save_model_path, save_model_architecture_path, save_model_weights_path):
    '''This function saves the trained model to the desired directory along with its weights
    and network architecture'''

    model.save(save_model_path)
    json_model = model.to_json()
    with open(save_model_architecture_path, 'w') as json_file:
        json_file.write(json_model)
    model.save_weights(save_model_weights_path)

def parse_arguments():
    parser = argparse.ArgumentParser(description='This script is a training script of the CNN')
    parser.add_argument(
        '-d',
        '--data_dir',
        type=str,
        default=None,
        help='Directory of the training data',
    )
    parser.add_argument(
        '-o',
        '--output_dir',
        type=str,
        default=None,
        help='Directory to which model is saved after training',
    )

    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())
