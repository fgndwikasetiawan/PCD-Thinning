import cv2
import numpy as np
import os
import sys

#fungsi untuk mengetahui apakah pixel pada baris i dan kolom j perlu di-flag
def filter1(img, i, j):
    if (img[i][j] == 255): #background
        return False

    N = 0
    for ii in range(i-1,i+2):
        for jj in range(j-1,j+2):
            try:
                if (img[ii][jj] == 0): #kalau tetangganya termasuk piksel contour
                    N += 1 #increment N
            except:
                pass
    if (N < 3) or (N > 7): #syarat pertama 3 < N < 7
        #print('N[%d][%d] = %d' % (i,j,N))
        return False
   # print('img[%d][%d] lolos syarat 1'% (i,j))
    S = 0
    if (int(img[i-1][j]) - int(img[i-1][j+1]) == 255): #p2-p3
        S += 1
    if (int(img[i-1][j+1]) - int(img[i][j+1]) == 255): #p3-p4
        S += 1
    if (int(img[i][j+1]) - int(img[i+1][j+1]) == 255): #p4-p5
        S += 1
    if (int(img[i+1][j+1]) - int(img[i+1][j]) == 255): #p5-p6
        S += 1
    if (int(img[i+1][j]) - int(img[i+1][j-1]) == 255): #p6-p7
        S += 1
    if (int(img[i+1][j-1]) - int(img[i][j-1]) == 255): #p7-p8
        S += 1
    if (int(img[i][j-1]) - int(img[i-1][j-1]) == 255): #p8-p9
        S += 1
    if (int(img[i-1][j-1]) - int(img[i-1][j]) == 255): #p9-p2
        S += 1
    #print('S: %d' % S)
    if (S != 1): #syarat kedua, S = 1
        return False

    #p2.p4.p6 = 0 (background)
    if (not(img[i-1][j] == 255 or img[i][j+1] == 255 or img[i+1][j] == 255)):
        return False

    #p4.p6.p8 = 0 (background
    if (not(img[i][j+1] == 255 or img[i+1][j] == 255 or img[i][j-1] == 255)):
        return False

    #print('img[%d][%d] flagged' % (i, j))

    return True

#fungsi untuk mengetahui apakah pixel pada baris i dan kolom j perlu di-flag
def filter2(img, i, j):
    if (img[i][j] == 255): #background
        return False

    N = 0
    for ii in range(i-1,i+2):
        for jj in range(j-1,j+2):
            if (img[ii][jj] == 0): #kalau tetangganya termasuk piksel contour
                N += 1 #increment N
    if (N < 3) or (N > 7): #syarat pertama 3 < N < 7
        return False
    S = 0
    if (int(img[i-1][j]) - int(img[i-1][j+1]) == 255): #p2-p3
        S += 1
    if (int(img[i-1][j+1]) - int(img[i][j+1]) == 255): #p3-p4
        S += 1
    if (int(img[i][j+1]) - int(img[i+1][j+1]) == 255): #p4-p5
        S += 1
    if (int(img[i+1][j+1]) - int(img[i+1][j]) == 255): #p5-p6
        S += 1
    if (int(img[i+1][j]) - int(img[i+1][j-1]) == 255): #p6-p7
        S += 1
    if (int(img[i+1][j-1]) - int(img[i][j-1]) == 255): #p7-p8
        S += 1
    if (int(img[i][j-1]) - int(img[i-1][j-1]) == 255): #p8-p9
        S += 1
    if (int(img[i-1][j-1]) - int(img[i-1][j]) == 255): #p9-p2
        S += 1
    #print('S: %d' % S)
    if (S != 1): #syarat kedua, S = 1
        return False

    #p2.p4.p8 = 0 (background)
    if (not(img[i-1][j] == 255 or img[i][j-1] == 255 or img[i][j+1] == 255)):
        return False

    #p2.p6.p8 = 0 (background
    if (not(img[i-1][j] == 255 or img[i+1][j] == 255 or img[i][j-1] == 255)):
        return False

    return True


#------------------------------------------------------------------------#

file_name = sys.argv[1]
img = False
try:
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    print ("Berhasil membaca gambar")
except Exception as ex:
    print ("Gagal membaca gambar! %s" % ex)

cv2.threshold(img, 128, 255, 8, img)

#iterasi filtering, lakukan iterasi sampai tidak ada yang bisa di-flag

max_iter = 50
iter_count = 1
flagged = 1
flag_matrix = np.zeros((img.shape[0], img.shape[1]), dtype=np.int8)

print ("Memulai iterasi, tekan ENTER untuk maju ke iterasi selanjutnya")

while (flagged > 0 and iter_count <= max_iter):
    print("Iterasi %d" % iter_count)
    iter_count += 1
    flagged = 0
    #step 1
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (filter1(img, i, j)):
                flagged += 1
                flag_matrix[i][j] = 1

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (flag_matrix[i][j] == 1):
                img[i][j] = 255

    flag_matrix = np.zeros((img.shape[0], img.shape[1]), dtype=np.int8)
    #step 2
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (filter2(img, i, j)):
                flagged += 1
                flag_matrix[i][j] = 1

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (flag_matrix[i][j] == 1):
                img[i][j] = 255
    print("Flagged: %d" % flagged)
    #cv2.destroyAllWindows()
    cv2.imshow("Gambar", img)
    cv2.waitKey()

print("Thinning selesai")
cv2.imshow("Gambar", img)
cv2.waitKey()
cv2.destroyAllWindows()
