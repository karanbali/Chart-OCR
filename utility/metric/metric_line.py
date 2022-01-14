#!/usr/bin/env python3

# NOTE: This file converts the predictions from Chart-OCR model into a file specific version that can be injected into ChartInfo-2020 Metric-6a
# Make sure to changes the paths according to your settings.
# This file assumes the availability for split-4 of official testing data of UB-PMC dataset


# The prediction output file from Chart-OCR is copied to the same directory and re-named as "pred.json"
# Then Run this file in the settings mentioned above.
# You'll get 2 folders (i.e. "gt" and "pred") that contains the predictions and ground-truths in the ChartInfo-2020 format.
# Finatlly, you can use "metric6a.py" file from ChartInfo-2020

import json
import os
import numpy as np
import os


type_opt = ['boxplots','lines','scatter points']




with open('./pred.json') as f:
    pred = json.load(f)

   
            
            
    for file in os.listdir('../data_test/split_4/images/'):
        
        
        
        try:
            if pred[file]:
                
                pd_i = pred[file]
            
                with open('../data_test/split_4/json/' + os.path.splitext(file)[0] + '.json') as f:
                    
                  gt_i = json.load(f)
                  
                  gt_type = gt_i['task1']['output']['chart_type']
                  
                  if gt_i['task6'] != None:
                     
                      with open('./gt/'+ os.path.splitext(file)[0] + '.json', 'w+') as outfile:
                          json.dump(gt_i, outfile)
                          
                      pd_i_new = gt_i
                      
                      
                              
                      if 'scatter' in gt_type.lower():
                          kp = []
                          for i in pd_i:
                              
                              line_d = []
                              for j in i:
                              
                                  bbox_dict = {"x": j[0], "y": j[1]}
                                  line_d.append(bbox_dict)
                                  
                              kp.append(line_d)
                              
                
                          
                          pd_i_new['task6']['output']['visual elements']['scatter points'] = kp
                          with open('./pred/'+ os.path.splitext(file)[0] + '.json', 'w+') as outfile:
                              json.dump(pd_i_new, outfile)
                              
                      elif 'line' in gt_type.lower():
                          kp = []
                          for i in pd_i:
                              
                              line_d = []
                              for j in i:
                              
                                  bbox_dict = {"x": j[0], "y": j[1]}
                                  line_d.append(bbox_dict)
                                  
                              kp.append(line_d)
                              
                
                          
                          pd_i_new['task6']['output']['visual elements']['lines'] = kp
                          with open('./pred/'+ os.path.splitext(file)[0] + '.json', 'w+') as outfile:
                              json.dump(pd_i_new, outfile)
                    
                          
                     
                          
                      
                      
        except:
            continue
                
                
           
    