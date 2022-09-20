# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 23:26:23 2022

@author: sarat
"""
#### This code will write the subtitle length to a dataframe. Subtitles can be using youtube link from https://downsub.com/
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta 

def find_subtitle_length(path, language = "Not provided", 
                         video_type = "Not provided", video_name = "Not provided"):
    file1 = open(path)
    Lines = file1.readlines()
    left_list = []
    right_list =[]
    time_diff_list = []
    for line in Lines:
        if ('-' in line) and ('>' in line):
            left_timing = line.split('-')[0]
            left_timing_2 = datetime.strptime(left_timing.strip(), '%H:%M:%S,%f')
            left_list.append(left_timing_2)
            
            right_timing = (line.split('>')[1]).strip()
            right_timing_2 = right_timing.replace('\n', '').strip()
            right_timing_3 = datetime.strptime(right_timing_2.strip(), '%H:%M:%S,%f')
            right_list.append(right_timing_3)
            
            time_diff = right_timing_3 - left_timing_2
            time_diff_secs = (time_diff.seconds*1.0) + ((time_diff.microseconds/1000000)*1.0)
            time_diff_list.append(time_diff_secs)
            

    df = pd.DataFrame(
        {'Video_language': language,
         'Video name': video_name, 
         'Video type': video_type,
         'left_timing': left_list,
         'right_timing': right_list,
         'time_diff_secs': time_diff_list
        })
    return df 
