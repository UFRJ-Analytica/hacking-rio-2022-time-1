import cv2 
import matplotlib.pyplot as plt
from imageio import imread
import numpy as np
import io
import base64
from .image_treatment import automatic_brightness_and_contrast
from PIL import Image

def contour_matching(img1, img2):
    """ Realiza o matching entre duas imagens a partir 
        da identificação dos contornos. """
    
    img1 = np.asarray(Image.open(io.BytesIO(base64.decodebytes(img1))))
    img2 = np.asarray(Image.open(io.BytesIO(base64.decodebytes(img2))))

    img1 = automatic_brightness_and_contrast(img1)
    img2 = automatic_brightness_and_contrast(img2)

    img_gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img_gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img_gray1=cv2.GaussianBlur(img_gray1, (11, 11), 0)
    img_gray2=cv2.GaussianBlur(img_gray2, (11, 11), 0)
    t, img_gray1=cv2.threshold(img_gray1, 150, 255, cv2.THRESH_BINARY)
    t, img_gray2=cv2.threshold(img_gray2, 150, 255, cv2.THRESH_BINARY)


    med_val1 = np.median(img_gray1)
    med_val2 = np.median(img_gray2)
    lower1 = int(max(0 ,0.7*med_val1))
    upper1 = int(min(255,1.3*med_val1))
    lower2 = int(max(0 ,0.7*med_val2))
    upper2 = int(min(255,1.3*med_val2))
    edges1 = cv2.Canny(img_gray1, lower1, upper1)
    edges2 = cv2.Canny(img_gray2, lower2, upper2)
    d2=cv2.matchShapes(edges1, edges2, cv2.CONTOURS_MATCH_I2, 0)
    # FLAN_INDEX_KDTREE = 1
    # index_params = dict(algorithm = FLAN_INDEX_KDTREE, trees=5)
    # search_params = dict(checks=50)

    # flann = cv2.FlannBasedMatcher(index_params, search_params)
    # matches = matchShapes(img1, img2, k=2)
    # matchesMask = [[0,0] for i in range(len(matches))]

    # for i,(m1, m2) in enumerate(matches):
    #     if m1.distance < 0.7 * m2.distance:
    #         matchesMask[i] = [1,0]
    
    # good_matches = []
    # for m1, m2 in matches:
    #     if m1.distance < 0.8 * m2.distance:
    #         good_matches.append([m1])

    return d2
