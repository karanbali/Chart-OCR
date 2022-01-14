#!/usr/bin/env python3

# This file is used to filter and convert the testing data of the UB-PMC-Line-class dataset into a Chart-OCR compatible version.
# This file specifically deals with Task-6a of ChartInfo-2020 for line, scatter and boxplots.


# Make sure to changes the paths according to your settings.
# This file assumes the availability of UB-PMC testing data in a folder named "data_test" in the current directory.
# So, just place the UB-PMC Testing folder in the current directory and re-name it to "data_test".

import json
import os
import numpy as np
import os
from PIL import Image

try:
    os.mkdir("./pmc_line")
    os.mkdir("./pmc_line/test2019")
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

  
        
for file in os.listdir('./data_test/split_4/images/'):
    
    
    
    with open('./data_test/split_4/json/' + os.path.splitext(file)[0] + '.json') as f:
      data = json.load(f)
      
      if 'task6' in data and data['task6'] != None:
          
          print(file)
          file_dir = './data_test/split_4/images/' + file
          img = Image.open(file_dir)
          w, h = img.size
          
          img.save('./pmc_line/test2019/' +file)
          
          file_dict = {"file_name": file, "height": h, "width": w, "id": id_cnt}
          #id_cnt += 1
          images.append(file_dict)
          
          data_d = data['task6']['output']['visual elements']
          
          for opt in type_opt:
              data_dict = data_d[opt]
              
              if opt == 'boxplots':
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
                          
                      bbox_dict = {"image_id": id_cnt, "category_id": 0, "bbox": bbox_line, "area": 0, "id": bbox_cnt}
                      bbox_dict_r = {"image_id": id_cnt, "category_id": 0, "bbox": [], "area": 0, "id": bbox_cnt}
                      bbox_cnt += 1
                      annotations.append(bbox_dict)
                      annotations_r.append(bbox_dict_r)
                  
                  
              else:
                  for i in data_dict:
                      
                      bbox_line = []
                      
                      for j in i:
                          bbox_line.append(j['x'])
                          bbox_line.append(j['y'])
                          
                      bbox_dict = {"image_id": id_cnt, "category_id": 0, "bbox": bbox_line, "area": 0, "id": bbox_cnt}
                      bbox_dict_r = {"image_id": id_cnt, "category_id": 0, "bbox": [], "area": 0, "id": bbox_cnt}
                      bbox_cnt += 1
                      annotations.append(bbox_dict)
                      annotations_r.append(bbox_dict_r)
              
    id_cnt += 1
              
              
json_d["images"] = images
json_d_r["images"] = images
json_d["annotations"] = annotations
json_d_r["annotations"] = annotations_r
json_d["categories"] = [{"supercategory": "Series", "id": 0, "name": "Series"}]
json_d_r["categories"] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


with open('./pmc_line/instancesLine(1023)_test2019.json', 'w+') as outfile:
    json.dump(json_d, outfile)
    
with open('./pmc_line/instancesLineClsReal(1119)_test2019.json', 'w+') as outfile:
    json.dump(json_d_r, outfile)

              
              

    