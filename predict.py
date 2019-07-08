from keras.models import load_model, model_from_json
from sklearn.feature_extraction.text import CountVectorizer
from datetime import timedelta
import time
import pandas as pd
import json
import logging
import tensorflow as tf

#Membuat inputan kalimat dengan separator |
sentence = input("Masukkan kalimat yang ingin di prediksi (gunakan | jika banyak) : \n")

sentence = sentence.split('|')

#Menghilangkan ERROR ataupun WARNING log tensorflow

tf.logging.set_verbosity(tf.logging.ERROR)

#Load dataset
data = pd.read_csv('Hasil_Sentimen.csv', index_col=None)
vectorizer = CountVectorizer()

#Load struktur model
json_file = open('model_cnn.json','r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)

#Load weight
loaded_model.load_weights('model.h5')
print('Loaded model from disk')

#Melakukan transform shape sesuai features dari dataset
vectorizer.fit_transform(data['tweets'].values)
test = vectorizer.transform(sentence)

#Melakukan predict
result = loaded_model.predict_classes(test,verbose=0)

#Menampilkan hasil
for i in range(len(result)):
	if (result[i] == 1):
		print(f"'{sentence[i]}' merupakan kalimat positif")
	else:
		print(f"'{sentence[i]}' merupakan kalimat negatif")	

