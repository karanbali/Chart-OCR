#!/usr/bin/env python3

# This file is used to filter and convert the training data of the UB-PMC-Line-class dataset into a Chart-OCR compatible version.
# This file specifically deals with Task-6a of ChartInfo-2020 for line, scatter and boxplots.

# Make sure to changes the paths according to your settings.
# This file assumes the availability of UB-PMC training data in a folder named "data" in the current directory.
# So, just place the UB-PMC Training folder in the current directory and re-name it to "data".

import json
import os
import numpy as np
import os
from PIL import Image


try:
    os.mkdir("./pmc_line")
    os.mkdir("./pmc_line/train2019")
except:
    print("No Directory created")

training_data_list = []

folder_opt = ['line']

type_opt = ['boxplots','lines','scatter points']

id_cnt = 0

bbox_cnt = 0

json_d = {}
json_d_r = {}
json_d["licenses"] = []
json_d_r["licenses"] = []

images = []

annotations = []
annotations_r = []



for folder in os.listdir('./data/images/'):

    #print(folder)
    if folder == ".DS_Store":
        continue
  
        
    for file in os.listdir('./data/images/' + folder):
        
        
        
        with open('./data/json/' + folder + '/' + os.path.splitext(file)[0] + '.json') as f:
          data = json.load(f)
          
          if 'task6' in data and data['task6'] != None:
          #if data['task6'] != null:
              
              print(file)
              file_dir = './data/images/' + folder + '/' + file
              img = Image.open(file_dir)
              w, h = img.size
              
              
              file_dict = {"file_name": file, "height": h, "width": w, "id": id_cnt}
              #id_cnt += 1
             
              
              data_d = data['task6']['output']['visual elements']
              
              if data_d['lines'] != [] or data_d['scatter points'] != [] or data_d['boxplots'] != []:
                  img.save('./pmc_line/train2019/' +file)
                  images.append(file_dict)
                  id_cnt += 1
              else:
                  continue
              
              for opt in type_opt:
                  data_dict = data_d[opt]
                  
                  if opt == 'boxplots' and data_d['boxplots'] != []:
                      for i in data_dict:
                          
                          bbox_line = []
                          
                          
                          bbox_line.append(i['first_quartile']['x'])
                          bbox_line.append(i['first_quartile']['y'])
                          bbox_line.append(i['max']['x'])
                          bbox_line.append(i['max']['y'])
                          bbox_line.append(i['median']['x'])
                          bbox_line.append(i['median']['y'])
                          bbox_line.append(i['min']['x'])
                          bbox_line.append(i['min']['y'])
                          bbox_line.append(i['third_quartile']['x'])
                          bbox_line.append(i['third_quartile']['y'])
                              
                          bbox_dict = {"image_id": id_cnt-1, "category_id": 0, "bbox": bbox_line, "area": 0, "id": bbox_cnt}
                          bbox_dict_r = {"image_id": id_cnt-1, "category_id": 0, "bbox": [], "area": 0, "id": bbox_cnt}
                          bbox_cnt += 1
                          annotations.append(bbox_dict)
                          annotations_r.append(bbox_dict_r)
                      
                      
                  elif data_d[opt] != []:
                      for i in data_dict:
                          
                          bbox_line = []
                          
                          for j in i:
                              bbox_line.append(j['x'])
                              bbox_line.append(j['y'])
                              
                          bbox_dict = {"image_id": id_cnt-1, "category_id": 0, "bbox": bbox_line, "area": 0, "id": bbox_cnt}
                          bbox_dict_r = {"image_id": id_cnt-1, "category_id": 0, "bbox": [], "area": 0, "id": bbox_cnt}
                          bbox_cnt += 1
                          annotations.append(bbox_dict)
                          annotations_r.append(bbox_dict_r)
                  
        
              
              
json_d["images"] = images
json_d_r["images"] = images
json_d["annotations"] = annotations
json_d_r["annotations"] = annotations_r
json_d["categories"] = [{"supercategory": "Series", "id": 0, "name": "Series"}]
json_d_r["categories"] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


with open('./pmc_line/instancesLine(1023)_train2019.json', 'w+') as outfile:
    json.dump(json_d, outfile)
    
with open('./pmc_line/instancesLineClsReal(1119)_train2019.json', 'w+') as outfile:
    json.dump(json_d_r, outfile)

              
              

    