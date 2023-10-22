import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def stretch_trap(trap, l=int(np.pi*480)):
    out_matrix = np.zeros_like(trap)
    for k in range(trap.shape[0]):
        string_without_nulls = trap[k,:,:][np.sum(trap[k,:,:], 1) != 0]
        out_matrix[k,:,:] = cv2.resize(string_without_nulls, (3,trap.shape[1]), interpolation = cv2.INTER_CUBIC)
    out_matrix = cv2.resize(out_matrix, (l, out_matrix.shape[0]), interpolation = cv2.INTER_CUBIC)
    return out_matrix
def stretch_sequence_of_traps(path = 'C:/Users/user/SCIENCE/HacatonTokomakDust/Tokodust/8.1', l=int(np.pi*480) ):
    out_image = stretch_trap(cv2.imread(path + '/'+os.listdir(path)[0]))
    for st in os.listdir(path):
        trap = stretch_trap(cv2.imread(path + '/{}'.format(st)))
        if trap is not None:
            out_image = cv2.vconcat([out_image, trap])
    return out_image
tag = 0
cv2.imwrite("2d_map_{}.png".format(tag), stretch_sequence_of_traps())


