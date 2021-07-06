import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

#tf.compat.v1.enable_eager_execution()

#teste
#src_path_train = "dataset-train-small/train/"
#src_path_test = "dataset-train-small/test/"

#Para videos
#src_path_train = "test_cnn_videos/train/"
#src_path_test = "test_cnn_videos/test"

#Para fotos
src_path_train = "test_cnn_photos/train/"
#src_path_test = "test_cnn_photos/test"

train_datagen = ImageDataGenerator(
        rescale=1 / 255.0)
        #rotation_range=20,
        #zoom_range=0.05,
        #width_shift_range=0.05,
        #height_shift_range=0.05,
        #shear_range=0.05,
        #horizontal_flip=True,
        #fill_mode="nearest",
        #validation_split=0.20)

#test_datagen = ImageDataGenerator(rescale=1 / 255.0)

#batch_size=2

train_generator = train_datagen.flow_from_directory(
    directory=src_path_train,
    target_size=(300, 300),
    color_mode="rgb",
    #batch_size=batch_size,
    class_mode="binary",
    subset='training',
    shuffle=False
    #seed=42
)

""" test_generator = test_datagen.flow_from_directory(
    directory=src_path_test,
    target_size=(300, 300),
    color_mode="rgb",
    batch_size=1,
    class_mode="binary",
    shuffle=False
    #seed=42
)  """


#X_train=np.concatenate([train_generator.next()[0] for i in range(train_generator.__len__())])
#y_train=np.concatenate([train_generator.next()[1] for i in range(train_generator.__len__())])
X=np.concatenate([train_generator.next()[0] for i in range(train_generator.__len__())])
y=np.concatenate([train_generator.next()[1] for i in range(train_generator.__len__())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

""" labels=[]

for label in train_generator.classes:
    temp=[]
    temp.append(label)
    labels.append(temp)
 """

#y_train=np.array(labels)

#classes = ["fake","real"]

""" def plot_sample(X,y,index):
    plt.figure(figsize= (15,2))
    plt.imshow(X[index])
    plt.xlabel(classes[int(y[index])])
    plt.show() """

#print(X_train[0]) #imagem 32x32,3 rgb channels
#print(y_train[0])
#plot_sample(X_train,y_train,0)


#construir a cnn
#A ReLu activation is applied after every convolution to transform the output values between the range 0 to 1. 
# #Max pooling is used to downsample the input representation
cnn = models.Sequential([
    layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(300, 300, 3)),
    layers.MaxPooling2D((2, 2)),
    
    layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    
    layers.Flatten(), #converts 3d feature map to 1d
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

cnn.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

cnn.fit(train_generator, epochs=10)

#print(cnn.evaluate(X_test,y_test))
#filenames= test_generator.filenames
#nb_samples = len(filenames)

#To use specific files to test
""" y_test=test_generator.classes
predict= cnn.predict(test_generator, steps=nb_samples)
print(predict)
y_pred = cnn.predict(X_test)
y_pred=cnn.predict(test_generator)
y_pred_classes = [np.argmax(element) for element in y_pred]
print(y_pred)
shape = len(y_pred)
value = 0
y_test = np.empty(shape, dtype=np.int)
y_test.fill(value) 

#print("Classification Report: \n", classification_report(y_test,predict))

#print(cnn.evaluate(test_generator,steps=nb_samples))"""

#To use the same dataset to train and test
predict=cnn.predict(X_test)
y_pred=np.argmax(predict, axis=1)
print("")
print('Confusion Matrix')
print(confusion_matrix(y_test,y_pred))
print("")
print('Classification Report')
target_names = ['Fake', 'Real']
print(classification_report(y_test, y_pred, target_names=target_names,zero_division=1))




