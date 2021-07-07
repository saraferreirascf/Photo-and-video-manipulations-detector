## How to:

- Create train file:
  - `$py create_train_file.py <dir> <features> <max_files> <output filename> `
   > **\<dir>** is the directory containing all multimedia files divided by two folders "fake" and "real" <br> **\<features>** is the number of features we want to extract from each file <br> **\<max_files>** stands for the number of the files that will be selected from each folder, meaning the minimum between the fake files and real files  <br> **\<output_filename>** is the desired train file name.
- Create test file:
  - `$py create_test_file.py <dir> <features> <max_files> <output filename> `
   > **\<dir>** is the directory containing all files target of classification <br> **\<features>** is the number of features we want to extract from each file (the same number of features of train file) <br> **\<max_files>** stands for the number of the files that will be selected from each folder, meaning the minimum between the fake files and real files  <br> **\<output_filename>** is the desired train file name.
- Run classification model:
  - `$py svm_model.py <train file> <test file> <k-fold option> `
  > **\<train file>** is the train file to train the SVM model <br> **\<test file>** is the file containing the files that we want to classify <br> **\<k-fold option>** explains how we want to run the model. <br>
  > There are 4 options for **\<k-fold option>** : <br>
  > - **-1** gives a classification for each object in test_file. 
  > - **0** split the train file in 2 parts: 67% for training and 33% for testing and gives an evaluation of the model.
  > - **5** 5-fold cross validation 
  > - **10** 10-fold cross validation

- Convert pkl file to txt:
  
  ``` py pkl_to_txt.py <pkl filename> <output filename> ```
  
- Convert pkl file to csv:

  ``` py pkl_to_csv.py <pkl filename> <output filename> ``` <br>
  *this script generates two .csv files. One for the features and one for the labels.
