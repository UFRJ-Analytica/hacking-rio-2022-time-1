import cv2
import numpy as np
import imutils

# image = cv2.imread("imgs/CM002/CM002F8.JPG")[1300:2400, 2100:3200]

# image = cv2.imread("imgs/Outras/greenturtleface1.jpg")
image = cv2.imread("imgs/Outras/turtle2.jpg")[:500, 100:700]
# image = cv2.imread("imgs/Outras/turtle3.jpg")[:300, :300]

# apenas para escalar a imagem se precisar
scale_percent = 1000 / image.shape[1]
width = int(image.shape[1] * scale_percent)
height = int(image.shape[0] * scale_percent)
image = cv2.resize(image, (width, height), interpolation = cv2.INTER_AREA)

# transformacoes
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img_gray, (11,11), 0)
edged = cv2.Canny(blurred, 30, 130, 3, L2gradient = True)
# Parametro 4: You can increase the Aperture size when you want to detect more detailed features.
# Parametro 5: Elimina um pouco dos reconhecimentos aleatorios 

contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
c = max(contours, key=cv2.contourArea)

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

cv2.imshow("final", image)
cv2.waitKey(0)