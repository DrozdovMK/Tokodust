import os
import cv2
import math
import numpy as np

def velocity(angle, peaks):
    #   frames  - матрица для каждого кадра со значением цветов RGB
    #   peaks   - положения пиков интенсивности на гранях отверстий
    #   angle   - угол поворота в рад (по часовой +, против -)

    new_peaks = []      # повернутая система координат k - номер кадра, i - номер пика,
    #   = координата пика
    dist = [[]]         # расстояния между пиками
    dx = 0              # сторона усеченной пирамиды

    for k in range(2):
        #dist.append()
        temp = []
        for i in range(3):
            temp.append((peaks[k][i][1]+peaks[k][i][0]/math.cos(angle[k]))*(math.cos(angle)+math.sin(angle[k])*math.tan(angle[k]))**(-1))
            try:
                dist[k][i] = temp[-1] - dist[k][i]
            except:
                pass
            dist[k].append(temp[-1])

        new_peaks.append(temp)

    #   проверка на потерю пика у края кадра
    if dist[0][0]>dist[1][0]:
        dx = new_peaks[0][1] - new_peaks[1][1]
    else:
        dx = new_peaks[0][0] - new_peaks[0][1]

    return dx # Кол-во пикселей

def trapezoid(frame, angle, dx):
    #   frames  - матрица для каждого кадра со значением цветов RGB
    #   angle   - угол поворота в рад (по часовой +, против -)

    center_x = round(len(frame)/2-1)
    center_y = round(len(frame[0])/2-1)

    radius = min(center_y,center_x)
    rad_inner = radius-dx

    trap=[]
    #frame_copy = frame.copy()
    row = -1
    d_phi = 2*math.pi/round(2*math.pi*center_y) if round(2*math.pi*center_y)!=0 else round(abs(2*math.pi*center_y-1))

    #if d_phi<2*math.pi/

    while radius > rad_inner:

        trap.append([])
        row += 1
        phi = math.pi/2-angle

        prev_px = []
        while phi < 2 * math.pi + math.pi/2-angle:
            #prev_px = []
            #print(round(center_x+radius*math.cos(math.pi/2+phi)), round(center_y-radius*math.sin(math.pi/2+phi)))
            #next_px = [round(center_x+radius*math.cos(math.pi/2+phi)), round(center_y-radius*math.sin(math.pi/2+phi))]
            next_px = [round(center_x+radius*math.cos(-math.pi/2-phi)), round(center_y+radius*math.sin(-math.pi/2-phi))]
            try:
                if prev_px != next_px:
                    #print(next_px[0],next_px[1])
                    trap[row].append(list(frame[next_px[0]][next_px[1]]))
            except:
                trap[row].append(list(frame[next_px[0]][next_px[1]]))

            # Новый круг
            prev_px = next_px.copy()
            phi += d_phi

        radius -= 1
        d_phi = 2*math.pi/(len(trap[row])-2)

    #print(trap)
    trap = fill(trap)

    return trap

def fill(arr):

    #del arr[0][0]
    max_len = len(arr[0])
    for row in range(1, len(arr)):
        #for col in range(len(arr[row], len(arr[0]))):
        #    arr[row].app
        arr[row] = [[0,0,0]] * int((max_len - len(arr[row]))/2) + arr[row] + [[0,0,0]] * int((max_len - len(arr[row])) / 2)
        if len(arr[row])!=max_len:
            arr[row].append([0,0,0]*(max_len - len(arr[row])))

    return arr
def kostyl(arr):
    for row in range(len(arr)):
        arr[row] = list(map(bgr_to_rgb, arr[row]))

def bgr_to_rgb(pixel):
    temp = [pixel[2],pixel[1],pixel[0]]
    return temp

def get_peaks(path):
    with open(path + "picks.txt", 'r') as file:
        f = file.readlines()
    arr = []
    for i in f:
        a = i.split()
        arrr = []
        for j in range(0, len(a), 2):
            arrr.append([int(a[j]), int(a[j+1])])
        arr.append(arrr)
    return arr

def normalnye_ugly(path):
    with open(path + "angle.txt", 'r') as file:
        f = file.read()
    arr = []
    array = f.split('.')
    a = array[0] + '.'
    b = ''
    for i in range(1, len(array)):
        if '-' in array[i]:
            b = array[i][-2] + '.'
            a += array[i][:-2]
        else:
            b = array[i][-1] + '.'
            a += array[i][:-1]
        arr.append(float(a))
        a = b

    return arr

def make_traps(path_to_frames):

    if not os.path.exists('./data_trap'):
        os.mkdir('./data_trap')

    angles = normalnye_ugly(path_to_frames)
    peaks = get_peaks(path_to_frames)

    i = 0
    for filename in os.listdir(path_to_frames):
        if '.png' in filename:
            pic = cv2.imread(path_to_frames+filename)
            #dx = velocity(angles, peaks[i:])
            pic2 = trapezoid(pic, angles[i], 5)
            kostyl(pic2)

            try:
                cv2.imwrite('./data_trap/'+'{:03d}.png'.format(i), np.array(pic2))
            except:
                pass
            i += 1