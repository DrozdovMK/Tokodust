import numpy as np
import scipy as sp
import cv2
import os
import time
import matplotlib.pyplot as plt
from pathlib import Path
from numpy.fft import fft2, ifft2, fftshift, ifftshift


def video_to_frames(path_input_video):
    print('\n\tVideo to Frames\n')
    start_time = time.time()
    path_video = "./data_video/"
    # i = 1
    if not os.path.exists(path_video):
        os.mkdir(path_video)
    path_video_frames = path_video + 'frames/'
    if not os.path.exists(path_video_frames):
        os.mkdir(path_video_frames)
    count = 0
    vidcap = cv2.VideoCapture(path_input_video)
    success, image = vidcap.read()
    success = True
    while success:
        print('=', end='', flush=True)
        # print ('Read a new frame: ', success)
        cv2.imwrite(path_video_frames + "frame_{:03d}.png".format(count), image)     # save frame as JPEG file
        count = count + 1
        success,image = vidcap.read()
    print('>\n')
    end_time = time.time()
    print("\n\tTime taken: {:.2f}\n".format(end_time-start_time))


def change_frames():
    print('\n\tUpdate frames\n')
    start_time = time.time()
    
    path_video = "./data_video/"
    path_frame = "./data_frames/"
    path_video_frames = path_video + 'frames/'
    if not os.path.exists(path_video):
        os.mkdir(path_video)
    if not os.path.exists(path_frame):
        os.mkdir(path_frame)
    if not os.path.exists(path_video_frames):
        os.mkdir(path_video_frames)
    folder = Path(path_video_frames)
    folder_size = len(list(folder.rglob("*")))
    for num in range(folder_size):
        try:
            print('=', end='', flush=True)
            im = cv2.imread(path_video_frames + "frame_{:03d}.png".format(num), cv2.IMREAD_GRAYSCALE).astype(float)
            # filter
            im_fft = fftshift(fft2(ifftshift(np.sqrt(im))))
            im_fft[239:241,319:321] = 0
            im_2 = ifftshift(ifft2(fftshift(im_fft)))
            im_2 = (abs(im_2)*abs(im_2)).astype(float)
            # normalize
            im_2_norm = 255 * im_2 / np.max(np.max(im_2))

            # suka blyat
            p = 0.7
            step = 10
            while True:
                im_2_ex = []
                for i in range(im_2_norm.shape[0]):
                    arr_ex = []
                    for j in range(im_2_norm.shape[1]):
                        if im_2_norm[i,j] > 255*p:
                            arr_ex.append(1)
                        else:
                            arr_ex.append(0)
                    im_2_ex.append(arr_ex)
                im_2_ex = np.array(im_2_ex)
                # p(d)icks
                x = []
                y = []
                x_1_list = []
                x_2_list = []
                for i in range(int(im_2_ex.shape[0]*0.7)):
                    if sum(im_2_ex[i]) > step:
                        x_1 = 0
                        x_2 = 0
                        k = 0
                        for j in range(1, im_2_ex.shape[1]):
                            if im_2_ex[i, j] == 1 and im_2_ex[i, j-1] == 0:
                                x_1 = j
                            elif im_2_ex[i, j] == 0 and im_2_ex[i, j-1] == 1 and j-x_1>step:
                                x_2 = j
                                break
                        if x_1 and x_2:
                            y.append(i)
                            x.append(int((x_1 + x_2)/2))
                            x_1_list.append(x_1)
                            x_2_list.append(x_2)
                if len(x) < 5:
                    p -= 0.05
                    continue
                # angles
                angles = []
                angles_1 = []
                for i in range(5, len(x)):
                    a = (x[i-5]-x[i])/abs(y[i]-y[i-5])
                    angles.append(a)
                    a_1 = (x_1_list[i-5]-x_1_list[i])/abs(y[i]-y[i-5])
                    angles_1.append(a_1)
                angle = np.arctan(np.mean(angles))
                angle_1 = np.arctan(np.mean(angles_1))

                # center of circle
                try:
                    x_0 = int((angle*x[-1] - angle_1*x_1_list[-1])/(angle-angle_1))
                    y_0 = int(angle*x_0 + y[-1] - angle*x[-1])
                    break
                except:
                    if p < 0.5:
                        step -= 1
                    else:
                        p -= 0.05
                    continue
            # ind of picks
            x_picks = []
            y_picks = []
            a = 0
            b = 0
            for i in range(1, len(y)):
                if y[i] - y[i-1] > 1:
                    b = i-1
                    j = int((a+b)/2)
                    x_picks.append(x[j])
                    y_picks.append(y[j])
                    a = i
                elif i == len(y) - 1:
                    b = i
                    j = int((a+b)/2)
                    x_picks.append(x[j])
                    y_picks.append(y[j])
            with open(path_frame + 'picks.txt', 'a') as file:
                # file.write(str(num))
                for a,b in zip(x_picks, y_picks):
                    file.write('{} {} '.format(a, b))
                file.write('\n')
            # update frame
            image = cv2.imread(path_video_frames + "frame_{:03d}.png".format(num))
            dx_0 = 320 - x_0
            dy_0 = 240 - y_0
            if dy_0 < 0:
                image_new_x = image[abs(dy_0):,:]
            else:
                image_new_x = image[:480-dy_0,:]
            if dx_0 > 0:
                image_new = image_new_x[:,:640-dx_0]
            else:
                image_new = image_new_x[:,abs(dx_0):]
            cv2.imwrite(path_frame + "frame_{:03d}.png".format(num), image_new)
            with open(path_frame + 'angle.txt', 'a') as file:
                file.write(str(angle))
        except:
            pass
    print('>\n')
    end_time = time.time()
    print("\n\tTime taken: {:.2f}\n".format(end_time-start_time))

