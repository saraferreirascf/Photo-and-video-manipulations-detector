# Deep-fake-detector :computer: :mag_right:

Deep fake detector is a plugin for Autopsy meant to detect deep fakes or even other types of image manipulations.
There are two versions of this plugin, one to detect maipulations on photos and another to detect manipulations on videos.

The autopsy module to detect manipulations in photos is described in Sara Ferreira, Mário Antunes, Manuel E. Correia; "Forensic analysis of tampered digital photos"; 25th Iberoamerican Congress on Pattern Recognition (CIARP); vol. XXXX; pp. A-B; Editor: Springer; May 2021; Porto; Portugal [To appear]

## Authors

Sara Ferreira - Department of Computer Science; Faculty of Sciences; University of Porto, 4169-007 Porto, Portugal; sara.ferreira@fc.up.pt
Mário Antunes - Computer Science and Communication Research Centre (CIIC), School of Technology and Management, Polytechnic of Leiria; 2411-901 Leiria; Portugal; mario.antunes@ipleiria.pt
Manuel E. Correira - INESC TEC, CRACS; 4200-465 Porto; Portugal, Department of Computer Science; Faculty of Sciences; University of Porto, 4169-007 Porto, Portugal;  mdcorrei@fc.up.pt

## Features

- Written in Python 3.9 
- Can detect both faces and objects
- Uses a recent method to extract features with DFT
- Uses machine learning to classify images

## Architecture

<img src="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/images/arquitetura-geral.png" alt="Click to download" width="600"/>

To obtain a functional deepfake detection system using Discrete Fourier Transform and Machine Learning, it is necessary for a first step to obtain the input data to feed the classification model, which will be used to classify each image as manipulated (deepfake) or legitimate. 

Pre-processing is depicted in Figure and consists initially of taking three to four frames per second from the input videos. This was achieved by creating a python script and all the frames extracted are added to the final dataset.
By having all the photos in the dataset, the features extraction are made by applying DFT method described in Section. The output is a labeled input datasets for both training and testing. The preprocessing phase reads the photos through the OpenCV library and further extracts their features. Using this method, exactly fifty features were obtained for each photo, that were then loaded into a new file with the corresponding label (0 for fake photos and 1 for the genuine ones). At the end of preprocessing phase, a fully labeled dataset is available and ready to feed the SVM model.

The processing phase corresponds to the SVM processing. In a first step, the following parameters were chosen: The RBF (Radial basis function) kernel and a regularization parameter of 3. This choice took into account the best practices adopted for similar experiments and the comparison with other parameters.
The implementation of SVM processing was made through scikit-learn library for Python 3.9.

The model created by SVM at the processing phase is then used to get a prediction for each photo in the testing dataset. The tests were carried on with a 10-fold cross-validation, by splitting the dataset into ten equal parts and using nine for training and one for testing. The dataset is balanced, regarding the number of fake and genuine photos and videos.

For each SVM model evaluation, the results obtained includes confusion matrix, precision and recall; and the calculated prediction that allows us to deduce the probability of an image have been manipulated.

The <a href="https://github.com/saraferreirascf/Deep-fake-detector/tree/main/Standalone_app" target="_blank">standalone application</a> architecture matches the Autopsy data source ingest module. The standalone application was developed before the Autopsy module, which gave the possibility to develop and test the method while disregarding the needed compatibility with the Python libraries and with the strict format that is required by Autopsy to the development of new modules.



## Installation

First you need to install <a href="https://www.autopsy.com/download/" target="_blank">Autopsy</a><br/>

After that, you need to download our detector. Click on your prefered software in order to get the correct version for you.<br/>


| Windows       | OSX           | Linux  |
| ------------- |:-------------:| -----:|
| <img src="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/images/windows.png" alt="Click to download" width="50" href="https://www.autopsy.com/download/" /> | <img src="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/images/apple.png" alt="Click to download" width="50" href="https://www.autopsy.com/download/"/> | <img src="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/images/linux.png" alt="Click to download" width="50" href="https://www.autopsy.com/download/"/> |

### Alternative

It is also possible to download the folder for each module
- <a href="https://github.com/saraferreirascf/Deep-fake-detector/tree/main/deepfake_video" target="_blank">DeepFake photo detector</a><br/>
- <a href="https://github.com/saraferreirascf/Deep-fake-detector/tree/main/deepfake_video" target="_blank">DeepFake video detector</a><br/>

Next, you need to unzip the rar and place the folder in the python plugin folder of Autopsy. In order do find that you can go to Autopsy > Tools > Python Plugins.

If you did everything well, now when you can see our plugin in the Autopsy when you do a ingest.

## Demo


