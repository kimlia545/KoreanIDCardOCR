import imgaug as ia # pip install imgaug
from imgaug import augmenters as iaa
#from files import *
import xml.etree.ElementTree as ET
from os import listdir
import cv2
import numpy as np
from pascal_voc_writer import Writer # pip install pascal-voc-writer

def read_anntation(xml_file: str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    bounding_box_list = []

    file_name = root.find('filename').text
    for obj in root.iter('object'):

        object_label = obj.find("name").text
        for box in obj.findall("bndbox"):
            x_min = int(box.find("xmin").text)
            y_min = int(box.find("ymin").text)
            x_max = int(box.find("xmax").text)
            y_max = int(box.find("ymax").text)

        bounding_box = [object_label, x_min, y_min, x_max, y_max]
        bounding_box_list.append(bounding_box)

    return bounding_box_list, file_name # [['name', 57, 75, 116, 99], ['number', 55, 101, 182, 123]] 56.jpg

def read_train_dataset(dir):
    images = []
    annotations = []

    for file in listdir(dir):
        if 'jpg' in file.lower() or 'png' in file.lower():
            images.append(cv2.imread(dir + file, 1))
            annotation_file = file.replace(file.split('.')[-1], 'xml')
            bounding_box_list, file_name = read_anntation(dir + annotation_file)
            annotations.append((bounding_box_list, annotation_file, file_name))

    images = np.array(images)

    return images, annotations

def image_aug(dir):
    ia.seed(1)

    images, annotations = read_train_dataset(dir)

    for idx in range(len(images)):
        image = images[idx]
        boxes = annotations[idx][0]

        ia_bounding_boxes = []
        for box in boxes:
            ia_bounding_boxes.append(ia.BoundingBox(x1=box[1], y1=box[2], x2=box[3], y2=box[4]))
        bbs = ia.BoundingBoxesOnImage(ia_bounding_boxes, shape=image.shape)

        seq = iaa.Sequential([
            iaa.Multiply((1.2, 1.5)),
            iaa.Affine(
                translate_px={"x": 40, "y": 60},
                scale=(0.5, 0.7)
            )
        ])

        seq_det = seq.to_deterministic()

        image_aug = seq_det.augment_images([image])[0]
        bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

        for i in range(len(bbs.bounding_boxes)):
            before = bbs.bounding_boxes[i]
            after = bbs_aug.bounding_boxes[i]
            print("BB %d: (%.4f, %.4f, %.4f, %.4f) -> (%.4f, %.4f, %.4f, %.4f)" % (
                i,
                before.x1, before.y1, before.x2, before.y2,
                after.x1, after.y1, after.x2, after.y2)
            )

        image_before = bbs.draw_on_image(image, thickness=20)
        image_after = bbs_aug.draw_on_image(image_aug, thickness=20, color=[0, 0, 255])

        cv2.imshow('test_image_before', cv2.resize(image_before, (380, 640)))
        cv2.imshow('test_image_after', cv2.resize(image_after, (380, 640)))

        cv2.waitKey(0)

def imgaug_generator(dir):
    ia.seed(1)

    images, annotations = read_train_dataset(dir)

    for idx in range(len(images)):
        image = images[idx]
        boxes = annotations[idx][0]

        ia_bounding_boxes = []
        for box in boxes:
            ia_bounding_boxes.append(ia.BoundingBox(x1=box[1], y1=box[2], x2=box[3], y2=box[4]))

        bbs = ia.BoundingBoxesOnImage(ia_bounding_boxes, shape=image.shape)

        seq = iaa.Sequential([
            iaa.Fliplr(0.5), # horizontal flips
            iaa.Crop(percent=(0, 0.1)), # random crops
            # Small gaussian blur with random sigma between 0 and 0.5.
            # But we only blur about 50% of all images.
            iaa.Sometimes(
                0.5,
                iaa.GaussianBlur(sigma=(0, 0.5))
            ),
            # Strengthen or weaken the contrast in each image.
            iaa.LinearContrast((0.75, 1.5)),
            # Add gaussian noise.
            # For 50% of all images, we sample the noise once per pixel.
            # For the other 50% of all images, we sample the noise per pixel AND
            # channel. This can change the color (not only brightness) of the
            # pixels.
            iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
            # Make some images brighter and some darker.
            # In 20% of all cases, we sample the multiplier once per channel,
            # which can end up changing the color of the images.
            iaa.Multiply((0.8, 1.2), per_channel=0.2),
            # Apply affine transformations to each image.
            # Scale/zoom them, translate/move them, rotate them and shear them.
            iaa.Affine(
                scale={"x": (0.9, 1.1), "y": (0.9, 1.1)}, # "x": (0.8, 1.2), "y": (0.8, 1.2
                translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)}, # "x": (-0.2, 0.2), "y": (-0.2, 0.2)
                rotate=(-10, 10), # (-25, 25)
                shear=(-6, 6) # (-8, 8)
            )
        ], random_order=True) # apply augmenters in random order

        seq_det = seq.to_deterministic()

        image_aug = seq_det.augment_images([image])[0]
        bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
        bbs_aug.remove_out_of_image().clip_out_of_image() #
        new_image_file = dir + 'result_' + annotations[idx][2]  #
        cv2.imwrite(new_image_file, image_aug)

        h, w = np.shape(image_aug)[0:2]
        voc_writer = Writer(new_image_file, w, h)

        for i in range(len(bbs_aug.bounding_boxes)):
            bb_box = bbs_aug.bounding_boxes[i]
            voc_writer.addObject(boxes[i][0], int(bb_box.x1), int(bb_box.y1), int(bb_box.x2), int(bb_box.y2))

        voc_writer.save(dir + 'result_' + annotations[idx][1]) # 

imgaug_generator('./train/') # dataset dir