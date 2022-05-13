#!/usr/bin/env python
# coding: utf-8

# ## Import Necessary libraries


import textseg as ts
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
import cv2
import json
import pandas as pd
import numpy as np
import glob
import os
import pytesseract
import math
import csv
import text_cleaning
import time

path_to_write = "TesseractDemo/Output/"


# ## The below function is to convert your pdf to image data

def convert_pdf_to_image(filepath, img_path_to_save):
    try:
        fileName = filepath.split("/")[-1].replace(".pdf", "")

        pages = convert_from_path(filepath, 350)
        i = 1
        for page in pages:
            image_name = img_path_to_save + fileName + "Page_" + str(i) + ".png"
            page.save(image_name, "JPEG")
            i = i + 1
        return {"status": 200, "response": "PDF Converted to image sucessfully", "fileName": fileName}
    except Exception as e:
        return {"status": 400, "response": str(e)}


# ## get the list of documents you want to pass as an input

documents = glob.glob("TesseractDemo/Input/*.pdf")


# ### The below function is used get the text present in a image

def text_from_tesseract(output_img):
    #pytesseract.image_to_pdf_or_hocr(output_img)
    text = str((pytesseract.image_to_string(output_img)))
    return text

# ### This function is the core function to process each pdf and store the resultant output using EASTTextdetectionModel
# ### Since we have passed only one document we are looking at the first index in a list


def read_write():
    head = final_text_opencv[0][0][0]
    head = text_cleaning.clean_tex(head)

    t = time.localtime()
    timetext =""
    timetext += str(t.tm_year) + "."
    timetext += str(t.tm_mon) + "."
    timetext += str(t.tm_mday) + "."
    timetext += str(t.tm_hour) + "."
    timetext += str(t.tm_min) + "."
    timetext += str(t.tm_sec)


    with open('TesseractDemo/' + str(head) + "." + str(timetext) + '.csv', 'w') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for head in final_text_opencv:
            now = time.strftime('%d-%m-%Y %H:%M:%S')
            writer.writerow([now, head])

        for final_text in final_text_opencv:
            print("----------------------------------")

            for page in final_text:
                for index in page:
                    print("DETECTED PARSE IS  :        ", page[index])
                    writer.writerow([page[index]])
                print("----------------------------------------------------------------")


data = pd.DataFrame()
final_name_list = []
final_text_opencv = []
final_text_tessaract = []

for i in documents:
    pdf = PdfFileReader(open(i, 'rb'))
    fname = i.split('\\')[1]
    print("TOTAL PAGE :            ", pdf.getNumPages())

    images = convert_from_path(poppler_path="C:/Users/dilat/poppler-0.67.0_x86/poppler-0.67.0/bin", pdf_path=i)
    resumes_img = []
    for j in range(len(images)):
        print("FILE NAME :            ", fname)
        print(path_to_write + fname.split('.')[0] + '_' + str(j) + '.jpg')
        # Save pages as images in the pdf
        images[j].save(path_to_write + fname.split('.')[0] + '_' + str(j) + '.jpg', 'JPEG')
        resumes_img.append(path_to_write + fname.split('.')[0] + '_' + str(j) + '.jpg')
    name_list = fname.split('.')[0] + '_' + '.jpg'

    text_opencv = []
    text_tessaract = []
    for i in resumes_img:
        frame = cv2.imread(i)
        os.remove(i)
        img = i.split("/")[2]

        output_img, label, dilate, c_dict, df1, split_img = ts.get_text_seg(frame, img)
        cv2.imwrite(path_to_write + img.split('.')[0] + ".png", output_img)
        for i in range(len(split_img)):
            cv2.imwrite(path_to_write + img.split('.')[0] + str(i) + ".png", split_img[i])

        text_opencv.append(c_dict)
        text_tessaract += text_from_tesseract(output_img)
        tesseract_str = ''.join(text_tessaract)

    final_name_list.append(name_list)
    final_text_opencv.append(text_opencv)
    final_text_tessaract.append(tesseract_str)

    read_write()

    final_name_list.clear()
    final_text_opencv.clear()
    final_text_tessaract.clear()
