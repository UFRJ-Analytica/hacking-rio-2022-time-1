import cv2 
import matplotlib.pyplot as plt
import numpy as np

from .image_treatment import automatic_brightness_and_contrast


def sift_feature_detection(img1):
    """ Identificar features locais de uma imagem utilizando 
        SIFT (scale-invariant feature transform). """

    img1 = automatic_brightness_and_contrast(img1)
    sift = cv2.SIFT_create()
    _, descriptors1 = sift.detectAndCompute(img1, None)

    return descriptors1


def flann_feature_matching(img1_descriptors, img2_descriptors):
    """ Com base nos descritores do SIFT de duas imagens, utilizar 
        o FLANN para compara-las. """

    FLAN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLAN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(img1_descriptors, img2_descriptors, k=2)
    matchesMask = [[0,0] for i in range(len(matches))]

    for i,(m1, m2) in enumerate (matches):
        if m1.distance < 0.7 * m2.distance:
            matchesMask[i] = [1,0]
    
    good_matches = []
    for m1, m2 in matches:
        if m1.distance < 0.8 * m2.distance:
            good_matches.append([m1])

    return good_matches

