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


folder_opt = ['horizontal_bar','vertical_bar']





with open('./pred.json') as f:
    pred = json.load(f)

    for file in os.listdir('../data_test/split_4/images/'):

        
        try:
            if pred[file]:
                
                pd_i = pred[file]
            
                with open('../data_test/split_4/json/' + os.path.splitext(file)[0] + '.json') as f:
                
                  gt_i = json.load(f)
                  
                  if 'task6' in gt_i and gt_i['task6'] != None and gt_i['task6']['output']['visual elements']['bars'] != []:
                     
                      with open('./gt/'+ os.path.splitext(file)[0] + '.json', 'w+') as outfile:
                          json.dump(gt_i, outfile)
                          
                      pd_i_new = gt_i
                      
                      bars = []
                      for i in pd_i:
                          
                          bbox_dict = {"height": i[3]-i[1], "width": i[2]-i[0], "x0": i[0], "y0": i[1]}
                
                          bars.append(bbox_dict)
                          
            
                      
                      pd_i_new['task6']['output']['visual elements']['bars'] = bars
                      with open('./pred/'+ os.path.splitext(file)[0] + '.json', 'w+') as outfile:
                          json.dump(pd_i_new, outfile)
        except:
            continue
                
                
           
    