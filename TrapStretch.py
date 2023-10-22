import cv2
import numpy as np
import os
def stretch_trap(trap, l=int(np.pi*480)):
    out_matrix = np.zeros_like(trap)
    for k in range(trap.shape[0]):
        string_without_nulls = trap[k,:,:][np.sum(trap[k,:,:], 1) != 0]
        out_matrix[k,:,:] = cv2.resize(string_without_nulls, (3,trap.shape[1]), interpolation = cv2.INTER_CUBIC)
    out_matrix = cv2.resize(out_matrix, (l, out_matrix.shape[1]), interpolation = cv2.INTER_CUBIC)
    return out_matrix
def stretch_sequence_of_traps(path = 'E:/Tokodust/data_frames/8.1/'):
    trap_1 = cv2.imread(path + '000.png')
    out_image = stretch_trap(trap_1)
    file_count = sum(len(files) for _, _, files in os.walk(path))
    for i in range(1,file_count):
        trap_1 = cv2.imread(path + '{:03d}.png'.format(i))
        out_image = cv2.vconcat([out_image, stretch_trap(trap_1)])
    return out_image

