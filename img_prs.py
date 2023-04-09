import pandas as pd
import numpy as np

import cv2
import matplotlib.pylab as plt



img1 = cv2.imread("frames\prueba.bmp")
#img2 = plt.imread("frames\outprueba"+str(j)+".bmp")

img_resize = cv2.resize(img1,None,fx=0.031,fy=0.032)

#fig, ax = plt.subplots(figsize=(8,8))
#ax.imshow(img_resize)
#print(str(img_resize.shape))

np.savetxt('matrices/rojos.txt',img_resize[:,:,0],fmt='%i',delimiter='\t')

#np.savetxt('matrices/azules.txt',img_resize[:,:,1],fmt='%i',delimiter='\t')
#np.savetxt('matrices/verdes.txt',img_resize[:,:,2],fmt='%i',delimiter='\t')
#plt.show()

c_pared = img_resize[:,:,0][0][0]
c_vacio = []
c_vacio.append(img_resize[:,:,0][1][1])
c_vacio.append(img_resize[:,:,0][1][2])
#snake_head = 245
#cabeza_s = img_resize[:,:,0][8][16]
serpiente = []
posicion_cab = 0

for i in img_resize[:,:,0][8]:
    if (i != c_vacio[0] and i != c_vacio[1]) and (i > 200):
        serpiente.append(i)

    if (i >=242 and i <= 247):
        posicion_cab += 1
        break
    posicion_cab += 1






