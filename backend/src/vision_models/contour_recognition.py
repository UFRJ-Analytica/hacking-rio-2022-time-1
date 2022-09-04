import cv2 
import matplotlib.pyplot as plt
import numpy as np

from .image_treatment import automatic_brightness_and_contrast


def contour_matching(img1, img2):
    """ Realiza o matching entre duas imagens a partir 
        da identificação dos contornos. """

    img1 = automatic_brightness_and_contrast(img1)
    img2 = automatic_brightness_and_contrast(img2)

    FLAN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLAN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(img1, img2, k=2)
    matchesMask = [[0,0] for i in range(len(matches))]

    for i,(m1, m2) in enumerate(matches):
        if m1.distance < 0.7 * m2.distance:
            matchesMask[i] = [1,0]
    
    good_matches = []
    for m1, m2 in matches:
        if m1.distance < 0.8 * m2.distance:
            good_matches.append([m1])

    return good_matches
