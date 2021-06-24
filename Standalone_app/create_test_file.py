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


    #var = input("Enter the directory of the images to test: ")
    #print("You entered: " + var)

    if os.path.isdir(dir) is False:
        print("this directory does not exist")
        exit(0)

    data= {}
    epsilon = 1e-8
    #N = 50
    y = []
    error = []


    #number_iter = 28 # max ficheiros por classe

    psd1D_total = np.zeros([number_iter, N])
    label_total = np.zeros([number_iter])
    psd1D_org_mean = np.zeros(N)
    psd1D_org_std = np.zeros(N)


    cont = 0

    #fake data
    #rootdir = dir+'/fake/'
    rootdir = dir
    for subdir, dirs, files in os.walk(rootdir):
        #print(files)
        for file in files:        
            #print("entrey boy fake")
            filename = os.path.join(subdir, file)
            if filename==dir+"/fake"+"\desktop.ini":
                continue
            
            img = cv2.imread(filename,0)
            
            # we crop the center
            #h = int(img.shape[0]/3)
            #w = int(img.shape[1]/3)
            #img = img[h:-h,w:-w]

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


    ## real data
    """ psd1D_total2 = np.zeros([number_iter, N])
    label_total2 = np.zeros([number_iter])
    psd1D_org_mean2 = np.zeros(N)
    psd1D_org_std2 = np.zeros(N) """


    cont = 0
    """ rootdir2 = dir+'/real/'
    #print(rootdir2)

    for subdir, dirs, files in os.walk(rootdir2):
        for file in files:        
            #print("entrey boy")
            filename = os.path.join(subdir, file)
            parts = filename.split("/")
            #print(filename)

            if filename==dir+"/real"+"\desktop.ini":
                break
    
            img = cv2.imread(filename,0)
        
            # we crop the center
            #h = int(img.shape[0]/3)
            #w = int(img.shape[1]/3)
            #img = img[h:-h,w:-w]

            f = np.fft.fft2(img)
            fshift = np.fft.fftshift(f)
            fshift += epsilon


            magnitude_spectrum = 20*np.log(np.abs(fshift))

            # Calculate the azimuthally averaged 1D power spectrum
            psd1D = radialProfile.azimuthalAverage(magnitude_spectrum)

            points = np.linspace(0,N,num=psd1D.size) # coordinates of a
            xi = np.linspace(0,N,num=N) # coordinates for interpolation

            interpolated = griddata(points,psd1D,xi,method='cubic')
            interpolated /= interpolated[0]

            psd1D_total2[cont,:] = interpolated             
            label_total2[cont] = 0 #todas fake
            cont+=1

            if cont == number_iter:
                break
        if cont == number_iter:
            break
        """

    """ for x in range(N):
        psd1D_org_mean2[x] = np.mean(psd1D_total2[:,x])
        psd1D_org_std2[x]= np.std(psd1D_total2[:,x]) """
        
        
    """ y.append(psd1D_org_mean)
    y.append(psd1D_org_mean2)

    error.append(psd1D_org_std)
    error.append(psd1D_org_std2)

    psd1D_total_final = np.concatenate((psd1D_total,psd1D_total2), axis=0)
    label_total_final = np.concatenate((label_total,label_total2), axis=0) """

    data["data"] = psd1D_total
    data["label"] = label_total

    #data to output to plugin

    #print(data)
    #return data
    #sys.stdout.write(data)

    output = open(output_filename, 'wb')
    pickle.dump(data, output)
    output.close()

    """ decision = input("do you really want to creathe the file? (y/n) ")
    if decision == 'y':
        output = open(test_filename, 'wb')
        pickle.dump(data, output)
        output.close()
        print("Test file created as", test_filename)
    else:
        exit(0) """
    print("DATA Saved")

if __name__ == "__main__":
    main()