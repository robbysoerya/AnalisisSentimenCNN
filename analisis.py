from __future__ import division
import csv
from string import punctuation


positive_word = []
negative_word = []
label = []
clean_tweets = []

header = [{"label","tweets"}]

tweets = open('ikan_asin.csv').read()

tweets_list = tweets.split('\n')

pos_sent = open("positif.txt").read()
positive_words = pos_sent.split('\n')

neg_sent = open("negatif.txt").read()
negative_words = neg_sent.split('\n')

for tweet in tweets_list:
	text_positif = []
	text_negatif = []
	positive_counter = 0
	negative_counter = 0

	tweet_preprocessing = tweet.replace('!','').replace('.','')
	tweet_processed = tweet_preprocessing.lower()

	for p in list(punctuation):
		tweet_processed = tweet_processed.replace(p,'')

	if tweet_processed:	
		clean_tweets.append(tweet_processed)

	words = tweet_processed.split(' ')

	word_count = len(words)

	for word in words:
		if word in positive_words:
			text_positif.append(word)
			positive_counter += 1
		elif word in negative_words:
			text_negatif.append(word)
			negative_counter += 1

	pos_count = (positive_counter / word_count) * 100		
	neg_count = (negative_counter / word_count) * 100

	print(pos_count,neg_count)
	if pos_count >= 0.5:
		label.append("1")
	else:
		label.append("2")	

output = zip(clean_tweets,label)
title = header
writer = csv.writer(open('Hasil_Sentimen.csv','w'))
writer.writerows(title)
writer.writerows(output)				
