# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 15:38:27 2022

@author: sarat
"""
from __future__ import unicode_literals
import speech_recognition as sr
import librosa
r = sr.Recognizer()
from googletrans import Translator
translator = Translator()
import datetime
import youtube_dl
import glob
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import textdistance


### download youtube video to local and 


def get_txt_subtitle(youtube_link):
    
    """" Download Video from youtube
        Input: Youtube Link
        Output: Downloads video to local in wav and returns the path"""
        
    directory = os.getcwd()
    print(directory)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_link])
        
    ### getting the latest file
    list_of_files = glob.glob('{}/*'.format(directory)) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file
    
    ### Getting Subtitle in txt format #######
    
def subtitile_txt(file_path, lan, chunk_time):
    """" Get Subtitle in txt format
           Input: File path to video in wav
           Output: string of subtitle"""
    
    len_audio = librosa.get_duration(filename=file_path)
    #print("Total length of audio is:{} secs".format(len_audio))
    chunks = int(len_audio/chunk_time)+1
    #print("Number of 3 sec chunks is {}".format(chunks))
    
    dic_translation = {}
    count = 1 
    while (count<chunks):
        ## load data to memory
        with sr.AudioFile(file_path) as source:
           # print(count)
            audio_data = r.record(source, offset = (count-1)*chunk_time, duration=chunk_time)
        # recognize (convert from speech to text)
            try:
                ## speech recognize
                text = r.recognize_google(audio_data, language=lan)
                #print(text)
                ### translate using google translate
                #print(translator.translate(text).text)
                dic_translation[count] = translator.translate(text).text
            except:
                dic_translation[count]= ''
            count = count+1
    sub_txt = ''
    for key in dic_translation:
        sub_txt = sub_txt +" " + dic_translation[key]
    return sub_txt



def read_ground_truth_subtitles(file_path):
    sub_txt_ground_truth = ''
    with open(file_path, encoding="utf8") as f:
        sub_txt_ground_truth = f.read().replace('\n', ' ')
    return sub_txt_ground_truth




    
def txt_pre_processing(string_to_be_preprocessed):
    """Input: Subtitle File to be pre-processed
        Output: List of processed words, stemmed words """
 
    ps = PorterStemmer()
    string_to_be_preprocessed = string_to_be_preprocessed.lower()
    words = word_tokenize(string_to_be_preprocessed)
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in words if not w.lower() in stop_words]

    filtered_sentence = []
  
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)

    stem_words = []
    non_stem_words = []
    non_stem_words = []
    for w in filtered_sentence:
        stem_words.append(ps.stem(w))
        non_stem_words.append(w)
    return stem_words, non_stem_words

def jacardian_distance(youtube_link, subtitle_ground_truth_path, lan):
    subtitle_path = get_txt_subtitle(youtube_link)
    sub_txt = subtitile_txt(subtitle_path, lan)
    sub_txt_ground_truth = read_ground_truth_subtitles(subtitle_ground_truth_path)
    predicted_stem, predicted_non_stem = txt_pre_processing(sub_txt)
    ground_truth_stem, ground_truth_non_stem = txt_pre_processing(sub_txt_ground_truth)
    ## 0.34
    print(textdistance.jaccard(predicted_stem , ground_truth_stem))
    ##0.3
    print(textdistance.jaccard(predicted_non_stem , ground_truth_non_stem))
    

##### Hindi Video Soch 
predicted_stem, predicted_non_stem = txt_pre_processing(sub_txt)
ground_truth_stem, ground_truth_non_stem = txt_pre_processing(sub_txt_ground_truth)

## 0.34
print(textdistance.jaccard(predicted_stem , ground_truth_stem))
##0.3
print(textdistance.jaccard(predicted_non_stem , ground_truth_non_stem))

### Hindi video Soch 2 
subtitle_path = get_txt_subtitle('https://www.youtube.com/watch?v=Pa3BV50PcLw&t=16s')
sub_txt = subtitile_txt(subtitle_path)
sub_txt_ground_truth = read_ground_truth_subtitles('C:/Users/sarat/Desktop/Subtitle_project/Subtitle File/Subtitle txt/Soch north indian south indian/soch_2.txt')
predicted_stem, predicted_non_stem = txt_pre_processing(sub_txt)
ground_truth_stem, ground_truth_non_stem = txt_pre_processing(sub_txt_ground_truth)
## 0.21
print(textdistance.jaccard(predicted_stem , ground_truth_stem))
## 0.18 
print(textdistance.jaccard(predicted_non_stem , ground_truth_non_stem))

######## Malayalam Videos
### Sujith - Wagah Border
### Stemmed value 0.29
### Non Stemmed value 0.26
jacardian_distance('https://www.youtube.com/watch?v=5tTS4-N___8', 'C:/Users/sarat/Desktop/Subtitle_project/Subtitle File/Subtitle txt/Sujith Malayalam - Wagah Border/sujith_wagah_border.txt', "ml-IN")


##### Changing Chunk time value ########
chunk_accuracy = []

subtitle_path = 'C:/Users/sarat/Desktop/Subtitle_project/Subtitle File/Subtitle txt/Soch north indian south indian/Who Are Indians _ Aryan Invasion Theory Explained-Pa3BV50PcLw.wav'
for chunk_time in [5, 10, 15, 20, 25, 30, 40]:
    sub_txt = subtitile_txt(subtitle_path, "hi-IN", chunk_time)
    sub_txt_ground_truth = read_ground_truth_subtitles('C:/Users/sarat/Desktop/Subtitle_project/Subtitle File/Subtitle txt/Soch north indian south indian/soch_2.txt')
    predicted_stem, predicted_non_stem = txt_pre_processing(sub_txt)
    ground_truth_stem, ground_truth_non_stem = txt_pre_processing(sub_txt_ground_truth)
    print(chunk_time)
    stem_similarity = textdistance.jaccard(predicted_stem , ground_truth_stem)
    ## 0.18 
    non_stem_similarity = textdistance.jaccard(predicted_non_stem , ground_truth_non_stem) 
    chunk_accuracy.append([chunk_time, stem_similarity, non_stem_similarity])
    chunk_accuracy
   [[5, 0.2453092425295344, 0.2132701421800948],
 [10, 0.24662402274342574, 0.22400558269364967],
 [15, 0.2421758569299553, 0.21590080233406272],
 [20, 0.16857360793287568, 0.15622641509433963],
 [25, 0.1778996865203762, 0.16421378776142526],
 [30, 0.13576415826221877, 0.12356101304681504],
 [40, 0.0831353919239905, 0.07716535433070866]]

