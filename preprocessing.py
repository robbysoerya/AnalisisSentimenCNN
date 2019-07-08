import tweepy
import re
import csv

#API Twitter
access_token = "132440583-NYeHdsPmR80oUPhNwFEtdTjDnd7XLUMi9eWg8r6P"
access_token_secret = "h21xqlNDy8hqyRH38T3HUYiTHPYjtDBD2eXGxFp1gCa2I"
consumer_key = "xS0xdqfSEjVFzsZp9v4yK3hbf"
consumer_secret = "Zxj6i0bvluqQF9Z1Ir3wziyheKB1WkuU1nQ8L41jUAMU8qzwH9"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

#Simpan hasil crawl twitter ke ikan_asin.txt
with open('ikan_asin.txt','w') as save_file:
    for tweet in tweepy.Cursor(api.search, q="indonesia -filter:retweets", tweet_mode="extended", lang="id").items(5000):
        text_tweet = tweet.full_text.encode("unicode_escape").decode()
        save_file.write(text_tweet)
        save_file.write("\n")
        print(text_tweet)

#Parse ikan_asin.txt ke list
with open('ikan_asin.txt','r') as open_file:
    text_tweet = [line.rstrip('\n') for line in open_file]

#Import library Sastrawi buat stemming bahasa Indonesia
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

#Deklarasi stop word
stopword_factory = StopWordRemoverFactory()
stopword = stopword_factory.create_stop_word_remover()

#Deklarasi stemming
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

#Ini untuk menghilangkan emoji
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#Fungsi untuk menghilangkan emoji
def strip_emoji(text):
    return emoji_pattern.sub(r'', text)

clean_tweets = []

#Membuat hasil crawl jadi bersih dari angka, ataupun simbol
for tweet in text_tweet:
  tweet = re.sub(r"(@[A-Za-z0-9]+)|(\w+:\/\/\S+)|(\\[Uu]\w+)|(\\n)", "", tweet)
  clean_tweets.append(strip_emoji(tweet))

#Menghilangkan stopword pada clean_tweets
filtered_tweets = []
for i in range(len(clean_tweets)):
  filtered = stopword.remove(clean_tweets[i])
  filtered_tweets.append(filtered)

#Melakukan stemming untuk menghilangkan imbuhan
stemmed_tweets = []
for i in range(len(filtered_tweets)):
  stemmed = stemmer.stem(filtered_tweets[i])
  stemmed_tweets.append(stemmed)

#Membuat file ikan_asin.csv dengan mode append
csvFile = open('ikan_asin.csv','a')
csvWriter = csv.writer(csvFile)

#Menyimpan hasil ke ikan_asin.csv
for i in range(len(stemmed_tweets)):
  csvWriter.writerow([stemmed_tweets[i]])

