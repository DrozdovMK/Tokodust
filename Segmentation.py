import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import segmentation



def GaussFilter(image, sigma = 400):
    mean = image.shape[1]//2
    sigma = 400
    x = np.arange(0,image.shape[1])
    gauss = 1 / np.sqrt(2*np.pi*sigma**2)*np.exp(-((x - mean)/(sigma))**2)
    gauss /= np.max(gauss)
    gauss3 = np.vstack((gauss, gauss, gauss))
    gauss3.shape
    image_filtered = np.copy(image).astype(float)
    for k in range(image.shape[0]):
        image_filtered[k, :] *= gauss3.T
    #plt.imshow(image_filtered.astype(np.uint8))
    return image_filtered.astype(np.uint8)

def Segmentize(image_filtered):
    
    gray_image = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)
    _, a = cv2.threshold(gray_image, 134, 255, cv2.THRESH_BINARY)
    bounds = segmentation.mark_boundaries(image_filtered, a,color=(240, 0, 0), mode = 'thick')
    plt.imshow(bounds)
    #cv2.imwrite('2dmap_1_with_Segments.png', bounds)
    return bounds

def Segmentize_without_plt(image_filtered):

    gray_image = cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY)
    _, a = cv2.threshold(gray_image, 134, 255, cv2.THRESH_BINARY)
    bounds = segmentation.mark_boundaries(image_filtered, a,color=(240, 0, 0), mode = 'thick')
    #plt.imshow(bounds)
    #cv2.imwrite('2dmap_1_with_Segments.png', bounds)
    return bounds