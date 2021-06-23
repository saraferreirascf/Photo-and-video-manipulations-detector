  
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
    if(len(sys.argv) != 2):
        print("Not enough arguments")
        print("insert dir to images")
        exit()

    var=sys.argv[1]

    if os.path.isdir(var) is False:
        print("this directory does not exist")
        exit(0)

    data= {}
    epsilon = 1e-8
    N = 50
    y = []
    error = []


    count_files=0

    for subdir, dirs, files in os.walk(var):
        for file in files:
            count_files=count_files+1
    
    
    number_files_fake=count_files
    
    psd1D_total = np.zeros([number_files_fake, N])
    label_total = np.zeros([number_files_fake])
    psd1D_org_mean = np.zeros(N)
    psd1D_org_std = np.zeros(N)

    cont = 0

    #fake data
    

    for subdir, dirs, files in os.walk(var):
        #print(files)
        for file in files:        
            #print("entrey boy fake")
            filename = os.path.join(subdir, file)
            
            img = cv2.imread(filename,0)
            
            # we crop the center
            h = int(img.shape[0]/3)
            w = int(img.shape[1]/3)
            img = img[h:-h,w:-w]

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

            if cont == number_files_fake:
                break
        if cont == number_files_fake:
            break

    data["data"] = psd1D_total.tolist()
    data["label"] = label_total.tolist()

    print(data) #output data for autopsy

    #Comment this when using autopsy
    #output = open("test_video_frames.pkl", 'wb')
    #pickle.dump(data, output)
    #output.close()


main()