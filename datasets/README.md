## Datasets
All datasets are labeled and balanced.

- <a href="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/datasets/train_frames_final.pkl" target="_blank">train_frames_final.pkl </a><br/> only contains the frames extracted from videos.
- <a href="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/datasets/train_photo_final.pkl" target="_blank">train_photo_final.pkl </a><br/> only contains photos.
- <a href="https://github.com/saraferreirascf/Deep-fake-detector/blob/main/datasets/train_video_and_photos_final.pkl" target="_blank">train_video_and_photos_final.pkl </a><br/> contains all photos and frames extracted from videos. 

### How to use them:

- In python 3:

  ``` pkl_file = open("train_photo_final.pkl", 'rb')
   data = pickle.load(pkl_file)
   pkl_file.close()
   X_train = data["data"]
   y_train= data["label"] 
