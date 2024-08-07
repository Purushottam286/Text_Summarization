import tkinter as tk
from PIL import Image , ImageTk 
from tkinter.filedialog import askopenfilename
import numpy as np
from tkinter.filedialog import askopenfile

from gtts import gTTS

import cv2 as cv

import matplotlib.image as mpimg

import os
import time
import random

import requests
import nltk



global fn
fn=""
##############################################+=============================================================

root = tk.Tk()
root.configure(background="Orchid1")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.geometry("%dx%d+0+0" % (w, h))
root.state('zoomed')
root.title("Document  Summarization")




#####
#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('back1.jpg')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)



#430
lbl = tk.Label(root, text="Document  Summarization", font=('times', 35,' bold '), height=1, width=60,bg="blue",fg="white")
lbl.place(x=1, y=2)



import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import PorterStemmer
from nltk.corpus import stopwords 
import math
from statistics import mean
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filepath', help="File Path", default="python.txt")
args = parser.parse_args()  

def frquency_matrix(sentences):
    matrix = {}
    stop_wrd = stopwords.words("english")
    stemmer = PorterStemmer()

    for sentence in sentences:
        sent_freq = {}
        words = word_tokenize(sentence)
        for word in words:
            word = word.lower()
            word = stemmer.stem(word)
            if word in stop_wrd:
                continue
            elif word in sent_freq.keys():
                sent_freq[word] += 1
            else:
                sent_freq[word] = 1

        matrix[sentence[:10]] = sent_freq
    return matrix


def term_freq_matrix(matrix_freq):
    term_freq = {}
    for s, table in matrix_freq.items():
        sent_table = {}

        word_count_in_sent = len(table)

        for word, freq in table.items():
            sent_table[word] = freq / word_count_in_sent

        term_freq[s] = sent_table

    return term_freq

def total_word_count(matrix_freq):
    total_word_freq = {}
    for sent, wtable in matrix_freq.items():
        for word, count in wtable.items():
            if word in total_word_freq.keys():
                total_word_freq[word] += 1
            else:
                total_word_freq[word] = 1

    return total_word_freq


def idf_matrix(matrix_freq, word_count, num_sent):
    idf = {}

    for sentence, freq in matrix_freq.items():
        idf_sent = {}

        for word in freq.keys():
            idf_sent[word] = math.log10(num_sent/ float(word_count[word]))

        idf[sentence] = idf_sent

    return idf

def tf_idf_matrix(term_freq_mat, matrix_idf):
    matrix_tf_idf = {}

    for (sentence1, tfreq1), (sentence2, tfreq2) in zip(term_freq_mat.items(), matrix_idf.items()):
        tf_idf_sent = {}

        for word, freq in tfreq1.items():
            freq2 = tfreq2[word]
            tf_idf_sent[word] = float(freq * freq2)

        matrix_tf_idf[sentence1] = tf_idf_sent

    return matrix_tf_idf

def sentence_scores(matrix_tf_idf):
    sent_score = {}

    for sent, tf_idf_matrix in matrix_tf_idf.items():
        total_score = 0
        word_count = len(tf_idf_matrix)

        for word, score in tf_idf_matrix.items():
            total_score = total_score + score

        sent_score[sent] = round(total_score/word_count, 2)

    return sent_score

def find_average_score(scores):
    avg_score = mean(scores[sent] for sent in scores)

    return round(avg_score, 2)

def generate_summary(sentences, scores, threshold):
    count = 0
    summary = ''

    print(round(threshold, 2))

    for sentence in sentences:
        if sentence[:10] in scores and scores[sentence[:10]] >= round(threshold, 2):
            summary = summary + " " + sentence
            count += 1

    return summary


    


global file

def sub():
   #  text = """
   #   Maria Sharapova has basically no friends as tennis players on the WTA Tour. The Russian player has no problems in openly speaking about it and in a recent interview she said: 'I don't really hide any feelings too much. 
   #   I think everyone knows this is my job here. When I'm on the courts or when I'm on the court playing, I'm a competitor and I want to beat every single person whether they're in the locker room or across the net.
   #   So I'm not the one to strike up a conversation about the weather and know that in the next few minutes I have to go and try to win a tennis match. 
   #   I'm a pretty competitive girl. I say my hellos, but I'm not sending any players flowers as well. Uhm, I'm not really friendly or close to many players.
   #   I have not a lot of friends away from the courts.' When she said she is not really close to a lot of players, is that something strategic that she is doing? Is it different on the men's tour than the women's tour? 'No, not at all.
   #   I think just because you're in the same sport doesn't mean that you have to be friends with everyone just because you're categorized, you're a tennis player, so you're going to get along with tennis players. 
   #   I think every person has different interests. I have friends that have completely different jobs and interests, and I've met them in very different parts of my life.
   #   I think everyone just thinks because we're tennis players we should be the greatest of friends. But ultimately tennis is just a very small part of what we do. 
   #   There are so many other things that we're interested in, that we do.'
   #   """
     file = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt')])
     if file is not None:
         text = file.read()
         print(text)
     
      
    # result_label1 = tk.Label(root, text=str(ARTICLE), width=50,height=20, font=("bold", 20),bg='white',fg='blue' )
     result_label1 = tk.Label(root, text="Article Text", width=10, font=("bold", 20),bg='purple',fg='white' )
     result_label1.place(x=230, y=100)      
     msg1=tk.Text(root, width=55,height=20, font=("bold", 15),bg='white',fg='black')
     msg1.place(x=15, y=150)
     msg1.insert(tk.END, str(text))
     
     # tts = gTTS(text=str(text), lang='en')
     # tts.save("good.mp3")
     # os.system("good.mp3")
     
     
     scrollbar = tk.Scrollbar(root, command=msg1.yview, cursor="heart")
     msg1['yscrollcommand'] = scrollbar.set
     scrollbar.place(x=625,y=150, height=465)    
     
     
    
      # path = args.filepath
      # with open(path, encoding="utf8") as f:
      #     text = f.read()
     sentences = sent_tokenize(text)
     num_sent = len(sentences)
       # print(sentences)

     matrix_freq = frquency_matrix(sentences)
       # for k,v in matrix_freq.items():
       #     print(k)
       #     print(v)
     term_freq_mat = term_freq_matrix(matrix_freq)
       # for k,v in term_freq_mat.items():
       #     print(k)
       #     print(v)
     word_count = total_word_count(matrix_freq)
       # for k,v in word_doc_count.items():
       #     print(k)
       #     print(v)
     matrix_idf = idf_matrix(matrix_freq, word_count, num_sent)
       # for k,v in matrix_idf.items():
       #     print(k)
       #     print(v)
     matrix_tf_idf = tf_idf_matrix(term_freq_mat, matrix_idf)
       # for k, v in matrix_tf_idf.items():
       #     print(k)
       #     print(v)
     scores = sentence_scores(matrix_tf_idf)
       # for k, v in scores.items():
       #     print(k)
[O       #     print(v)
     avg_score = find_average_score(scores)

     summary = generate_summary(sentences, scores, 0.9*avg_score)
     
     tts = gTTS(text=str(summary), lang='en')
     tts.save("good.mp3")
     os.system("good.mp3")

     print(summary)
[I     with open("summary.txt",'w') as f:
         f.write(summary)

     
     #res = summarizer(chunks, min_length = 0.1 * len(chunks), max_length = 0.2 * len(chunks)

     
     result_label1 = tk.Label(root, text="Summary Text", width=15, font=("bold", 20),bg='purple',fg='white' )
     result_label1.place(x=890, y=100)   
    
     msg=tk.Text(root, width=55,height=20, font=("bold", 15),bg='white',fg='black')
     msg.place(x=725, y=150)
     
     
     
     msg.insert(tk.END, summary)
     scrollbar = tk.Scrollbar(root, command=msg.yview, cursor="heart")
     msg['yscrollcommand'] = scrollbar.set
     scrollbar.place(x=1335,y=150, height=465)
     # with open('blogsummary.txt', 'w') as f:
     #     f.write(text1)
        
        
def window():
    root.destroy()
        
# button2=tk.Button(root,foreground="white",background="black",font=("Tempus Sans ITC",14,"bold"),text="Upload text",command=upload,width=15,height=2)
# button2.place(x=5,y=100) 
button1 = tk.Button(root, text=" Upload File  ", command=sub,width=13, height=1, font=('times', 15, ' bold '),bg="green",fg="black")
button1.place(x=280, y=650)

exit = tk.Button(root, text="Exit", command=window, width=5, height=1, font=('times', 15, ' bold '),bg="red",fg="black")
exit.place(x=1200, y=650)



  root.mainloop():
