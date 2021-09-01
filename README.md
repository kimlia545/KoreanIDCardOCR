# KoreanIDCardOCR
Korean ID Card OCR using YOLO and Tesseract

## Step 1  Generate Data 
### Genrator Korean ID Card  
![0](https://user-images.githubusercontent.com/72369991/131650895-0dc4c5dc-b925-4f5c-8f74-948f27d5ae6f.jpg)

## Step 2 Data Labeling
### [ImgLabel](https://github.com/tzutalin/labelImg)  
 ![imgaug](https://user-images.githubusercontent.com/72369991/131650855-546bb674-7bb0-481c-8a0c-a4bcfde52623.png)
 
## Step 3 Data Augmentation
### [ImgAug](https://github.com/aleju/imgaug)  
![result_0](https://user-images.githubusercontent.com/72369991/131650885-3d6d27bf-7e34-408c-9aa5-3c497f8e5053.jpg)

## Step 4 Upload your data in roboflow
### [Roboflow](https://roboflow.com/)  
To import custom images and bounding boxes in the YOLO format, use Roboflow.

## Step 5 Yolo (Text Detection)
### [yolo5](https://colab.research.google.com/drive/1gDZ2xcTOgR39tGGs-EZ6i3RTs16wmzZQ)  
### [yolo4](https://colab.research.google.com/drive/1mzL6WyY9BRx4xX476eQdhKDnd_eixBlG#scrollTo=GNVU7eu9CQj3)

## Step 6 Text Recognition
### [Tesseract](https://github.com/tesseract-ocr/tesseract)  
### [deep-text-recognition-benchmark korean model](https://github.com/parksunwoo/ocr_kor)
