# GStreamer-with-Tensorflow
This project is forked from https://github.com/jackersson/gst-plugins-tf. The objective of this project is to perform inference using GStreamer without worrying about how to set the GStreamer plugin environment.

## Installation
```
$ sudo apt-get install cmake
$ sudo pip3 install -r requirements.txt
```

## How To Use
1. Prepare a .mp4 video and named it as video.mp4. Place it at the same directory as main.py.
2. Download the Tensorflow model from here https://drive.google.com/drive/folders/1SDOByrtB4bKAeiKisTvNbP-z0KxkvXul?usp=sharing.
3. Extract and move the model into /data directory, so it has this structure:
|---data
|   |---models
|   |   |---ssdlite_mobilenet_v2_coco_2018_05_09
|   |---mscoco_label_map.yml
|   |---tf_object_api_cfg.yml
You may try another Tensorflow model with Tensorflow Models Zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) and labels (https://github.com/tensorflow/models/tree/master/research/object_detection/data)
4. From the main directory, you can execute:
$ python3 main.py

## Result
![alt text](https://github.com/jefflgaol/GStreamer-with-Tensorflow/blob/master/test.png)
