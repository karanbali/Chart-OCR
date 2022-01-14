#!/usr/bin/env python3


# This file is used to filter and convert the training data of the UB-PMC-Line-class dataset into a Chart-OCR compatible version.
# This file specifically deals with Phase-3: Training Ensemble models.

# Make sure to changes the paths according to your settings. Especially constants "DATA_DIR" and "SAVE_DIR"
# This file assumes the availability of UB-PMC training data in a folder named "data" in the current directory.
# So, just place the UB-PMC Training folder in the current directory and re-name it to "data".
# Different splits with their image and annotations data will be saved in the "SAVE_DIR"
# Different splits will follow a specific naming pattern, where first (split-0) will have "0" as a prefix and subsequently fifth split (split-4) will have "4" as prefix.



import json
import os
import numpy as np
import os
from PIL import Image

training_data_list = []

#folder_opt = ['horizontal_bar','vertical_bar']
type_opt = ['boxplots','lines','scatter points']



final = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}

final[0]['id_cnt'] = 0
final[0]['bbox_cnt'] = 0
final[0]['dict'] = {}
final[0]['dict']['licenses'] = []
final[0]['dict']['images'] = []
final[0]['dict']['annotations'] = []
final[0]['dict']['categories'] = [{"supercategory": "Series", "id": 0, "name": "Series"}]

final[1]['id_cnt'] = 0
final[1]['bbox_cnt'] = 0
final[1]['dict'] = {}
final[1]['dict']['licenses'] = []
final[1]['dict']['images'] = []
final[1]['dict']['annotations'] = []
final[1]['dict']['categories'] = [{"supercategory": "Series", "id": 0, "name": "Series"}]

final[2]['id_cnt'] = 0
final[2]['bbox_cnt'] = 0
final[2]['dict'] = {}
final[2]['dict']['licenses'] = []
final[2]['dict']['images'] = []
final[2]['dict']['annotations'] = []
final[2]['dict']['categories'] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


final[3]['id_cnt'] = 0
final[3]['bbox_cnt'] = 0
final[3]['dict'] = {}
final[3]['dict']['licenses'] = []
final[3]['dict']['images'] = []
final[3]['dict']['annotations'] = []
final[3]['dict']['categories'] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


final[4]['id_cnt'] = 0
final[4]['bbox_cnt'] = 0
final[4]['dict'] = {}
final[4]['dict']['licenses'] = []
final[4]['dict']['images'] = []
final[4]['dict']['annotations'] = []
final[4]['dict']['categories'] = [{"supercategory": "Series", "id": 0, "name": "Series"}]


split_cnt = 0


DATA_DIR = './data/'

SAVE_DIR = './line_splits/'


for folder in os.listdir(DATA_DIR+'images'):

    #print(folder)
    if folder == ".DS_Store":
        continue
  

    #if folder in folder_opt:
    if 'scatter' in folder.lower() or 'line' in folder.lower():
        
        print(folder)
        
        
        for file in os.listdir(DATA_DIR +'images/'+ folder):
            
            split = split_cnt%5
            
            
            
            
            
            
            print(file)
            file_dir = DATA_DIR +'images/'+ folder + '/' + file
            img = Image.open(file_dir)
            w, h = img.size
            file_dict = {"file_name": file, "height": h, "width": w, "id": final[split]['id_cnt']}
            
            
            
            
            with open(DATA_DIR+'json/' + folder + '/' + os.path.splitext(file)[0] + '.json') as f:
              data = json.load(f)
              
              
              
              if 'task6' in data and data['task6'] != None:
                  
                  
                  
                  
                  data_d = data['task6']['output']['visual elements']
                  
                  if data_d['lines'] != [] or data_d['scatter points'] != [] or data_d['boxplots'] != []:
                      if not os.path.exists(SAVE_DIR+ str(split) +'/train2019/'):
                          os.makedirs(SAVE_DIR+ str(split) +'/train2019/')
                          
                      img.save(SAVE_DIR+ str(split) +'/train2019/'+ file)
                      
                      
                
                      final[split]['dict']['images'].append(file_dict)
                      final[split]['id_cnt'] += 1
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
                                  
                              bbox_dict = {"image_id": final[split]['id_cnt']-1, "category_id": 0, "bbox": bbox_line, "area": 0, "id": final[split]['bbox_cnt']}
                              final[split]['bbox_cnt'] += 1
                              split_cnt += 1
                              final[split]['dict']['annotations'].append(bbox_dict)
                            
                          
                          
                      elif data_d[opt] != []:
                          for i in data_dict:
                              
                              bbox_line = []
                              
                              for j in i:
                                  bbox_line.append(j['x'])
                                  bbox_line.append(j['y'])
                                  
                              bbox_dict = {"image_id": final[split]['id_cnt']-1, "category_id": 0, "bbox": bbox_line, "area": 0, "id": final[split]['bbox_cnt']}
                              final[split]['bbox_cnt'] += 1
                              split_cnt += 1
                              final[split]['dict']['annotations'].append(bbox_dict)
                    
                  
                    
                  
              




for ind in range(5):
    with open(SAVE_DIR+str(ind)+'_instancesLine(1023)_train2019.json', 'w+') as outfile:
        json.dump(final[ind]['dict'], outfile)

              
              

    