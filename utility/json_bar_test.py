#!/usr/bin/env python3

# This file is used to filter and convert the testing data of the UB-PMC-Line-class dataset into a Chart-OCR compatible version.
# This file specifically deals with Task-6a of ChartInfo-2020 for bar class.

# Make sure to changes the paths according to your settings.
# This file assumes the availability of UB-PMC testing data in a folder named "data_test" in the current directory.
# So, just place the UB-PMC Testing folder in the current directory and re-name it to "data_test".

import json
import os
import numpy as np
import os
from PIL import Image


try:
    os.mkdir("./pmc_bar")
    os.mkdir("./pmc_bar/test2019")
except:
    print("No Directory created")

training_data_list = []

folder_opt = ['horizontal_bar','vertical_bar']



id_cnt = 0

bbox_cnt = 0

json_d = {}
json_d["licenses"] = []

images = []

annotations = []


for file in os.listdir('./data_test/split_4/images/'):

    with open('./data_test/split_4/json/' + os.path.splitext(file)[0] + '.json') as f:
      data = json.load(f)
      
      if 'task6' in data and data['task6'] != None and data['task6']['output']['visual elements']['bars'] != []:
          
          print(file)
          file_dir = './data_test/split_4/images/' + file
          img = Image.open(file_dir)
          w, h = img.size
          
          img.save('./pmc_bar/test2019/'+file)
          
          file_dict = {"file_name": file, "height": h, "width": w, "id": id_cnt}
          #id_cnt += 1
          images.append(file_dict)
          
          data_dict = data['task6']['output']['visual elements']['bars']
          
          for i in data_dict:
              
              bbox_dict = {"image_id": id_cnt, "category_id": 0, "bbox": [i['x0'], i['y0'], i['x0']+i['width'], i['y0']+i['height']], "area": i['height']*i['width'], "id": bbox_cnt}
              bbox_cnt += 1
              annotations.append(bbox_dict)
            
            
            
            

                  
    id_cnt += 1              
                      
              
              
json_d["images"] = images
json_d["annotations"] = annotations
json_d["categories"] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


with open('./pmc_bar/instancesBar(1031)_test2019.json', 'w+') as outfile:
    json.dump(json_d, outfile)

              
              

    