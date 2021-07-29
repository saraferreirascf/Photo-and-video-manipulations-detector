  
#///////////////////////////////////////////////////////////////////////#
#                                                                       #
#                                                                       #
#                  Script to generate test data v1                      #
#           Extract features with Discrete Fourier Transform            #
#                                                                       #
#      Sara Ferreira [sara (dot) ferreira (at) fc (dot) up (dot) pt]    #
#                                                                       #  
#                                                                       #  
#                                                                       #
#///////////////////////////////////////////////////////////////////////#

# Contact: Sara Ferreira [sara (dot) ferreira (at) fc (dot) up (dot) pt]
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import cv2
import numpy as np
import os
import sys
import radialProfile
import glob
from matplotlib import pyplot as plt
import pickle
from random import randrange
from scipy.interpolate import griddata



def main():
    if(len(sys.argv) != 5):
        print("Not enough arguments")
        print("insert <dir> <features> <max_files> <output filename>")
        exit()

    dir=sys.argv[1]
    N=int(sys.argv[2])
    number_iter=int(sys.argv[3])
    output_filename=str(sys.argv[4])+".pkl"

    if os.path.isdir(dir) is False:
        print("this directory does not exist")
        exit(0)

    data= {}
    psd1D_total = np.zeros([number_iter, N])
    label_total = np.zeros([number_iter])
    psd1D_org_mean = np.zeros(N)
    psd1D_org_std = np.zeros(N)


    cont = 0
    rootdir = dir
    for subdir, dirs, files in os.walk(rootdir):
        #print(files)
        for file in files:        
            #print("entrey boy fake")
            filename = os.path.join(subdir, file)
            if filename==dir+"\desktop.ini":
                continue
            
            img = cv2.imread(filename,0)
            f = np.fft.fft2(img)
            fshift = np.fft.fftshift(f)

            magnitude_spectrum = 20*np.log(np.abs(fshift))
            psd1D = radialProfile.azimuthalAverage(magnitude_spectrum)

            # Calculate the azimuthally averaged 1D power spectrum
            points = np.linspace(0,N,num=psd1D.size) # coordinates of a
            xi = np.linspace(0,N,num=N) # coordinates for interpolation

            interpolated = griddata(points,psd1D,xi,method='cubic')
            interpolated /= interpolated[0]

            psd1D_total[cont,:] = interpolated             
            label_total[cont] = 0 #fake
            cont+=1

            if cont == number_iter:
                break
        if cont == number_iter:
            break

                
    for x in range(N):
        psd1D_org_mean[x] = np.mean(psd1D_total[:,x])
        psd1D_org_std[x]= np.std(psd1D_total[:,x])


    data["data"] = psd1D_total
    data["label"] = label_total

    output = open(output_filename, 'wb')
    pickle.dump(data, output)
    output.close()


    print("DATA Saved")

if __name__ == "__main__":
    main()
