
import sys
import os
import logging # Writing logs to file and console
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import load_model
from argparse import ArgumentParser
from tensorflow.keras.preprocessing.image import ImageDataGenerator # For working with images without loading them all into memory

#==================================================================================================
#                                            LOGGER
#==================================================================================================

logger = logging.getLogger()
lprint = logger.info
wprint = logger.warning

def setup_logger(output_dir):
    log_formatter = logging.Formatter('%(message)s')

    logfile_path = os.path.join(output_dir, 'dataset.log')
    file_handler = logging.FileHandler(logfile_path)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)


#==================================================================================================
#                                     DATA PREPROCESSING 
#==================================================================================================


def get_image_generators(training_dir, validation_dir, batch_size, spectrogram_size,
                         ):
    train_datagen = ImageDataGenerator()
    train_generator = train_datagen.flow_from_directory(training_dir,
                                                        batch_size=batch_size,
                                                        target_size=spectrogram_size,
                                                        shuffle=False)
     

    validation_datagen = ImageDataGenerator()
    validation_generator = validation_datagen.flow_from_directory(validation_dir,
                                                                  batch_size=batch_size,
                                                                  target_size=spectrogram_size,
                                                                  shuffle=False)

    classes = validation_generator.class_indices.keys()
    class_count = len(classes)

    return train_generator, validation_generator, classes, class_count

#==================================================================================================
#                                       VISUALISATIONS 
#==================================================================================================

def heatmap(data, row_labels, col_labels, ax=None, cbar_kw={}, cbarlabel="",
            disable_annotations=False, **kwargs):

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xlabel("Prediction")
    ax.set_ylabel("Label")
    # ... and label them with the respective list entries.
    if disable_annotations:
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', bottom=False, top=False, left=False,
                        right=False, labelleft=False)
    else:
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)
        ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)

        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def annotate_heatmap(im, data=None, textcolors=("black", "white")):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    threshold = im.norm(data.max()) / 2.

    # Set default alignment to center
    kw = dict(horizontalalignment="center", verticalalignment="center")

    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, data[i, j], **kw)
            texts.append(text)

    return texts

def load_eng_labels(classes):
    labels = list()
    for label in classes:
        labels.append(label.split('(')[0])

    labels = np.array(labels, dtype=object)
    return labels

def print_confusion_matrix(y_pred, y_true, classifications, output_dir, experiment_id,
                           disable_annotations=True):
    confusion_mtx = tf.math.confusion_matrix(y_true, y_pred, num_classes=len(classifications))

    fig, ax = plt.subplots(figsize=(12, 10))
    im, cbar = heatmap(confusion_mtx, classifications, classifications, ax=ax,
                       cmap=plt.cm.GnBu, cbarlabel="Classification",
                       disable_annotations=disable_annotations)
    if not disable_annotations:
        annotate_heatmap(im)

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{experiment_id}_confusion.png'))
    plt.clf()


#==================================================================================================
#                                    MAIN FUNCTION 
#==================================================================================================

def size_tuple(txt):
    values = txt.split('x')
    return int(values[0]), int(values[1])

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--training_dir', required=True, type=str,
                        help='Directory containing training data.')
    parser.add_argument('-v', '--validation_dir', required=True, type=str,
                        help='Directory containing validation data.')
    parser.add_argument('-o', '--output_dir', required=True, type=str,
                        help='Directory to which network and visualisations will be saved')
    parser.add_argument('-i', '--experiment_id', required=True, type=str,
                        help='Part of the experiment name, it will be concatenated with network name')
    parser.add_argument('-n', '--network', type=str, required=True,
                        help='File with neural network')
    parser.add_argument('--spectrogram_size', type=size_tuple, default=(100,100),
                        help='Size of spectrogram')
    parser.add_argument('--batch_size', type=int, default=10,
                        help='Number of images in single batch')
    parser.add_argument('--disable_annotation', action='store_true',
                        help='If set confusion matrix will not be annotated, usefull for large datasets')
    return parser.parse_args()

def main(args):
    setup_logger(args.output_dir)
    if len(tf.config.list_physical_devices('GPU')) == 0:
        logger.fatal('Unable to find GPU, stopping execution.')
    train_generator, validation_generator, classes, class_count = get_image_generators(args.training_dir,
                                                                                       args.validation_dir, 
                                                                                       args.batch_size,
                                                                                       args.spectrogram_size)
    model = load_model(args.network)
    labels = validation_generator.class_indices.keys()
    print(labels)
    y_pred_1 = np.argmax(model.predict(train_generator), axis=1)
    y_pred_2 = np.argmax(model.predict(validation_generator), axis=1)
    y_pred = np.hstack([y_pred_1, y_pred_2])
    y_true = np.hstack([train_generator.classes, validation_generator.classes])
    print(f'{y_pred.shape}  --  {y_true.shape}')
    print_confusion_matrix(y_pred, y_true, classes, args.output_dir, args.experiment_id,
                           args.disable_annotation)

if __name__ == '__main__':
    main(parse_arguments())

