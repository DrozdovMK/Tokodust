import cv2
import numpy as np

def stretch_trap(trap, l):
    out_matrix = np.zeros_like(trap)
    for k in range(trap.shape[0]):
        string_without_nulls = trap[k,:,:][np.sum(trap[k,:,:], 1) != 0]
        out_matrix[k,:,:] = cv2.resize(string_without_nulls, (3,trap.shape[1]), interpolation = cv2.INTER_CUBIC)
    out_matrix = cv2.resize(out_matrix, (l, out_matrix.shape[1]), interpolation = cv2.INTER_CUBIC)
    return out_matrix