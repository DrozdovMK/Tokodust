import numpy as np
import scipy as sp
import cv2
import os
import time
import matplotlib.pyplot as plt
from pathlib import Path
from numpy.fft import fft2, ifft2, fftshift, ifftshift

from trans_rot import video_to_frames, change_frames
from trapezoid import make_traps, kostyl
from TrapStretch import stretch_sequence_of_traps
import Segmentation

def Main(path_to_the_video):
    #
    video_to_frames(path_to_the_video)
    change_frames()

    make_traps('./data_frames/')

    map2d = stretch_sequence_of_traps('./data_trap')

    map2d = Segmentation.GaussFilter(map2d)
    map2d = Segmentation.Segmentize_without_plt(map2d)
    #kostyl(map2d_2)
    #map2d = (map2d+map2d_2).astype(np.uint8)


    if not os.path.exists('./maps'):
        os.mkdir('./maps')
    cv2.imwrite('./map.png', map2d)

if __name__ == "__main__":
    Main('E:/Tokodust/data_video/Endoscope video (12).mp4')

#%%
