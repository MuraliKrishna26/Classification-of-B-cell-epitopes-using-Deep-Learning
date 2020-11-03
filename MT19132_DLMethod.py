# -*- coding: utf-8 -*-
"""KaggleAssignment3_Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eFCug2rPfRCbOIwdqia0e0i1t-TYnIU4
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split

train_data =  "//content//drive//My Drive//BDMH//Assignment 3//trainset.data"
test_data  =  "//content//drive//My Drive//BDMH//Assignment 3//testset.dat"

def getdata(path):
  sequence = []
  label_convert = []

  with open(path) as f:
    for line in f:
      text_file = line.split(",")
      sequence.append(text_file[0])
      s = text_file[1]
      s = s[:-1]
      label_convert.append(s)

  sequence = sequence[1:]        
  label_convert = label_convert[1:] 

  label = []

  for item in label_convert:
    if item == '+1':
        label.append(1)
    else:
        label.append(-1)

  return sequence,label

X_tr, Y_train = getdata(train_data)

aminoacid_sequence = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']

dipeptide_seq = []

for charone in aminoacid_sequence:
  for chartwo in aminoacid_sequence:
    char_to_add = charone+chartwo
    dipeptide_seq.append(char_to_add)

# dipeptide_seq

def get_dipeptite_dictionary(str):
  size = len(str)
  i = 0

  eachseq_list = []
  while( i < size - 1 ):
    add_seq = str[i] + str[i+1]
    eachseq_list.append(add_seq)
    i += 1
  
  getdict = {}

  for item in eachseq_list:
    if getdict.get(item) == None:
      getdict[item] = 1
    else:
      temp = getdict[item]
      temp += 1
      getdict[item] = temp

  new_dict = {}
  for item in getdict:
    value = getdict[item]
    value = value/(len(str) - 1)
    new_dict[item] = value

  return new_dict

def getlist_of_dictionary(X_tr):
  list_dictionary = []

  for each in X_tr:
    dic = get_dipeptite_dictionary(each)
    list_dictionary.append(dic)

  return list_dictionary

def getvector(vector_dictionary):
  final_vector = []

  for dic in vector_dictionary:

    vec = [0.0] * 400

    for item in dic:

      for seq in dipeptide_seq:
        if seq == item:
          index = dipeptide_seq.index(seq)
          vec[index] = dic[item]

    final_vector.append(vec)

  return final_vector

training_vector_dictionary = getlist_of_dictionary(X_tr)

X_train = getvector(training_vector_dictionary)

len(X_train)

len(Y_train)

x = np.array(X_train)
y = np.array(Y_train)

x.shape

y.shape

x_train, x_val, y_train, y_val = train_test_split(x,y, test_size=0.3, random_state=42)

y_train_final = []
for i in y_train:
  if i == -1:
    y_train_final.append(0)
  else:
    y_train_final.append(1)

y_train_final = np.array(y_train_final)

y_val_final = []
for i in y_val:
  if i == -1:
    y_val_final.append(0)
  else:
    y_val_final.append(1)

y_val_final = np.array(y_val_final)

len(y_val_final)

len(y_train_final)

## x_train
## x_val

## y_val_final
## y_train_final





from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.optimizers import Adam

model = Sequential([
                    Dense(16, input_shape = (400,), activation='relu'),
                    Dense(32, activation = 'relu'),
                    Dense(2, activation = 'softmax')
                    ])

model.summary()

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train,y_train_final,batch_size=10, epochs=15)



y_val_predict = model.predict_classes(x_val)

y_val_predict



y_val_final

from sklearn.metrics import accuracy_score

accuracy_score(y_val_final,y_val_predict)















from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.layers import Flatten

model_new = Sequential([Flatten(),
                    Dense(512, activation='relu'),
                    Dense(256, activation = 'relu'),
                    Dense(128, activation = 'relu'),
                    Dense(2, activation = 'softmax')
                    ])

model_new.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model_new.fit(x_train,y_train_final, epochs=15)



y_val_predict = model_new.predict_classes(x_val)

accuracy_score(y_val_final,y_val_predict)







## Now Test with test data

test_data  =  "//content//drive//My Drive//BDMH//Assignment 3//testset.dat"

test_seq = []
with open(test_data) as f:
  for line in f:
    text_file = line.split(",")
    test_seq.append(text_file[1][:-1])

X_te = test_seq[1:]

# X_te

testing_vector_dictionary = getlist_of_dictionary(X_te)

X_test = getvector(testing_vector_dictionary)

X_test = np.array(X_test)

Y_predict =  model_new.predict_classes(X_test)



final_test = []
for i in Y_predict:
  if i == 0:
    final_test.append(-1)
  else:
    final_test.append(1)



count = 1001
for i in final_test:
  print(count,',',i, sep='')
  count += 1

