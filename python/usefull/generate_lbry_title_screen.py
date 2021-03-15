'''
This script is used for generating a title card for LBRY uploads.
You can open a video and then go through it frame by frame and write image files from
those frames.
When using this script you may press "s" to save current frame as a jpg file, "q" to
quit script or any other key to progress video by amount given in a frame skip argument.
'''
import argparse
import sys
import cv2


def main(args):
    '''
    This is script main function, for more details see module description.

    Parameters
    ----------
        args: argparse.Namespace
            A namespace containing all arguments from command line or their default
            values.

    Returns
    -------
        None
    '''
    video = cv2.VideoCapture(args.input_video)
    if video is None:
        print(f'Unable to open {args.input_video}.')
        sys.exit()
 
    frame_read, frame = video.read()
    image_count = 0
    frames_to_skip = 0
    while frame_read:
        if frames_to_skip == 0:
            cv2.imshow('Video frame', frame)
            key = cv2.waitKey(0)
            if key == ord('s'):
                cv2.imwrite(f'{image_count}.jpg', frame)
                image_count += 1
            elif key == ord('q'):
                break
            frames_to_skip = args.frame_skip
        else:
            frames_to_skip -= 1
        frame_read, frame = video.read()
 
    video.release()
    cv2.destroyAllWindows()


def parse_arguments():
    '''
    This function parses arguments from command line.

    Returns
    -------
        arparse.Namespace
        This is a namespace that contains arguments from command line.
    '''
    parser = argparse.ArgumentParser(description=('Script for extracting frames from '
        'videos. Created with LBRY title card generation in mind.'
        'When running program use "s" to save current frame to file, "q" to quit'
        'or any other key to progress video.'))
    parser.add_argument('-i',
            '--input_video',
            type=str,
            required=True,
            help='Video that will be processed'
            )
    parser.add_argument('-s',
            '--frame_skip',
            type=int,
            default=1,
            help='How many frames are skipped with a button press.'
            )
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
