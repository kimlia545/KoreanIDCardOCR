# -*- coding: utf-8 -*-
import numpy as np
import cv2
from PIL import ImageFont, ImageDraw, Image
import os

face_dir = './face/'
face_list = os.listdir(face_dir)

name_f = open('./name.txt','r',encoding='utf-8')
name_lines = name_f.readlines()
number_f = open('./number.txt','r',encoding='utf-8')
number_lines = number_f.readlines()
address_f = open('./address.txt','r',encoding='utf-8')
address_lines = address_f.readlines()
date_f = open('./date.txt','r',encoding='utf-8')
date_lines = date_f.readlines()

output_dir = './result/'

alpha = 0.3

for i in range(10):
    background = cv2.imread('./background.jpg')
    # face 
    face = cv2.imread(face_dir+face_list[i])
    face_resize = cv2.resize(face, (130, 153), interpolation = cv2.INTER_CUBIC)
    b_row = 20
    b_cols = 245
    rows, cols, channel = face_resize.shape
    roi = background[b_row:rows+b_row, b_cols:cols+b_cols] # [230:358, 17:173] 
    img2gray = cv2.cvtColor(face_resize, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 200, cv2.THRESH_BINARY) #  10, 255
    mask_inv = cv2.bitwise_not(mask)
    background_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    face_resize_fg = cv2.bitwise_and(face_resize, face_resize, mask=mask)

    blended = background_bg * alpha + face_resize_fg * (1-alpha)
    blended = blended.astype(np.uint8) 
    dst = cv2.addWeighted(background_bg, alpha, face_resize_fg, (1-alpha), 0) 
    #dst = cv2.add(background_bg, face_resize_fg) #######

    background[b_row:rows+b_row, b_cols:cols+b_cols] = dst

    # text
    background = Image.fromarray(background)
    fontpath = "fonts/gulim.ttc" 
    title_font = ImageFont.truetype(fontpath, size=25)
    name_font = ImageFont.truetype(fontpath, size=19)
    number_font = ImageFont.truetype(fontpath, size=17)
    address_font = ImageFont.truetype(fontpath, size=13)
    date_font = ImageFont.truetype(fontpath, size=14)
    city_font = ImageFont.truetype(fontpath, size=17)
    draw = ImageDraw.Draw(background)
    
    name = name_lines[i][:-1]
    number = number_lines[i][:-1]
    address = address_lines[i][:-1]
    date = date_lines[i][:-1]
    city = "부산특별시 부산구청장"
    words_list = address.split()
    if len(words_list) >= 5:
        address_1 = str(words_list[0]) + ' ' + str(words_list[1]) 
        address_2 = str(words_list[2]) + ' ' + str(words_list[3]) 
        address_3 = str(words_list[4])
    elif len(words_list) == 4:
        address_1 = str(words_list[0]) + ' ' + str(words_list[1]) 
        address_2 = str(words_list[2]) + ' ' + str(words_list[3]) 
    else:
        address_1 = str(words_list[0]) + ' ' + str(words_list[1]) 
        address_2 = str(words_list[2]) 
    
    draw.text((60,75), name ,font=name_font,fill=(0,0,0))
    draw.text((60,105), number ,font=number_font,fill=(0,0,0))
    draw.text((45,130), address_1 ,font=address_font,fill=(0,0,0))
    draw.text((45,145), address_2 ,font=address_font,fill=(0,0,0))
    try:
        draw.text((45,160), address_3 ,font=address_font,fill=(0,0,0))
    except:
        pass
    draw.text((145,180), date ,font=date_font,fill=(0,0,0))
    draw.text((110,200), city ,font=city_font,fill=(0,0,0))
    background = np.array(background)
    cv2.imwrite(output_dir+str(i)+'.jpg', background)
    #cv2.imshow('result', background)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
