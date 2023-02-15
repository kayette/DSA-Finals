import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import collections
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

lyrics = pd.read_csv("taylor_swift_lyrics_2006-2022_all.csv")

lyrics.head()
lyrics.info()
print(lyrics.album_name.unique())

def album_release(row):  
    if row['album_name'] == 'Taylor Swift':
        return '2006'
    elif row['album_name'] == 'Fearless (Taylor’s Version)':
        return '2008'
    elif row['album_name'] == 'Speak Now (Deluxe)':
        return '2010'
    elif row['album_name'] == 'Red (Deluxe Edition)':
        return '2012'
    elif row['album_name'] == '1989 (Deluxe)':
        return '2014'
    elif row['album_name'] == 'reputation':
        return '2017'
    elif row['album_name'] == 'Lover':
        return '2019'
    elif row['album_name'] == 'evermore (deluxe version)':
        return '2020'
    elif row['album_name'] == 'folklore (deluxe version)':
        return '2021'
    elif 'midnights' in row['album_name']:
        return '2022'
    
    return 'No Date'

lyrics['album_year'] = lyrics.apply(lambda row: album_release(row), axis=1)
lyrics.head()

lyrics['clean_lyric'] = lyrics['lyric'].str.lower()
lyrics['clean_lyric']= lyrics['clean_lyric'].str.replace('[^\w\s]','')
lyrics.head()
stop = ['the', 'a', 'this', 'that', 'to', 'is', 'am', 'was', 'were', 'be', 'being', 'been']
lyrics['clean_lyric'] = lyrics['clean_lyric'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
lyrics.head()

lyrics['clean_lyric_list'] = lyrics['clean_lyric'].apply(lambda x: x.split())
print(lyrics.head())

lyrics['clean_lyric_list_rejoined'] = lyrics['clean_lyric_list'].apply(lambda x: ' '.join(x))
print(lyrics.head())

lyrics.drop(['clean_lyric_list', 'clean_lyric_list_rejoined'], axis=1, inplace=True)
print(lyrics.head())

lyrics['midnight'] = lyrics['clean_lyric'].str.contains('midnight')
sum(lyrics['midnight'])

#keywords
night = ['night','midnight', 'dawn', 'dusk', 'evening', 'late', 'dark', '1am', '2am', '3am', '4am']
day = ['day', 'morning', 'light', 'sun', 'dawn', 'noon', 'golden', 'bright']
love = ['love', 'lover', 'heart', 'like', 'hello', 'hi']
hurt = ['hurt', 'scared', 'cry', 'tears', 'goodbye', 'broken']
time = ['today', 'tomorrow', 'yesterday']

night_regex = '|'.join(night)
day_regex = '|'.join(day)
love_regex = '|'.join(love)
hurt_regex = '|'.join(hurt)
time_regex = '|'.join(time)

lyrics['night'] = lyrics['clean_lyric'].str.contains(night_regex)
lyrics['day'] = lyrics['clean_lyric'].str.contains(day_regex)
lyrics['love'] = lyrics['clean_lyric'].str.contains(love_regex)
lyrics['hurt'] = lyrics['clean_lyric'].str.contains(hurt_regex)
lyrics['time'] = lyrics['clean_lyric'].str.contains(time_regex)

night_count = sum(lyrics['night'])
day_count = sum(lyrics['day'])
love_count = sum(lyrics['love'])
hurt_count = sum(lyrics['hurt'])
time_count = sum(lyrics['time'])

print("night words: ", night_count)
print("day words: ", day_count)
print("love words: ", love_count)
print("hurt words: ", hurt_count)
print("time words: ", time_count)

lyrics.head()

yearly_mentions = lyrics.groupby('album_year').sum().reset_index()
yearly_mentions

plt.plot(yearly_mentions['album_year'], yearly_mentions['night'])
plt.title("Taylor Swift Night Mentions")
plt.show()

year_name = pd.read_csv('album_year_name.csv')

yearly_mentions.sort_values(by='album_year', ascending=True, inplace=True)
year_name.sort_values(by='album_year', ascending=True, inplace=True)
yearly_mentions['album_name'] = year_name['album_name']

yearly_mentions.sort_values(by='night', ascending=False)
yearly_mentions.sort_values(by='day', ascending=False)

plt.plot(yearly_mentions['album_year'], yearly_mentions['night'], label = 'night')
plt.plot(yearly_mentions['album_year'], yearly_mentions['day'], label = 'day')
plt.title("Taylor Swift Day vs. Night Mentions")
plt.legend()
plt.show()

yearly_mentions.sort_values(by='album_year', ascending=True, inplace=True)
year_name.sort_values(by='album_year', ascending=True, inplace=True)
yearly_mentions['album_name'] = year_name['album_name']

yearly_mentions.sort_values(by='love', ascending=False)
yearly_mentions.sort_values(by='hurt', ascending=False)

plt.plot(yearly_mentions['album_year'], yearly_mentions['love'], label = 'love')
plt.plot(yearly_mentions['album_year'], yearly_mentions['hurt'], label = 'hurt')
plt.title("Taylor Swift Love vs. Hurt Mentions")
plt.legend()
plt.show()

lyrics['position'] = lyrics['track_n'] + (lyrics['line']/1000)
positional_mentions = lyrics.groupby('position').sum().reset_index()

fig = plt.gcf()
fig.set_size_inches(18,8)

plt.plot(positional_mentions['position'], positional_mentions['night'], label = 'night')
plt.plot(positional_mentions['position'], positional_mentions['day'], label = 'day')
plt.legend()
plt.title("Day vs. Night Mentions by Album Position")
plt.show()

lyrics['lyrics_tok'] = lyrics['clean_lyric'].str.split(' ')
lyrics.head()

word_list = [word for list_ in lyrics['lyrics_tok'] for word in list_]

word_frequency = collections.Counter(word_list)
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
word_frequency

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()
sia.polarity_scores("I love Taylor Swift!")

lyrics['polarity'] = lyrics['clean_lyric'].apply(lambda x: sia.polarity_scores(x))
lyrics.head()

lyrics[['neg', 'neu', 'pos', 'compound']] = lyrics['polarity'].apply(pd.Series)
lyrics.drop('polarity', axis=1)
lyrics.head()

pos = sum(lyrics['pos'])
neg = sum(lyrics['neg'])
compound = sum(lyrics['compound'])

print("positive: ", pos)
print("negative: ", neg)
print("compound: ", compound)

yearly_sentiment = lyrics.groupby('album_year').sum().reset_index()
plt.plot(yearly_sentiment['album_year'], yearly_sentiment['compound'])
plt.title("Taylor Swift's average Album Sentiment")
plt.show()

night = lyrics[lyrics['night']==True]
day = lyrics[lyrics['day']==True]
love = lyrics[lyrics['love']==True]
hurt = lyrics[lyrics['hurt']==True]

print("\n\nNight: ",len(night))
print("Day: ",len(day))
print("Love: ",len(love))
print("Hurt: ",len(hurt))

night_sentiment = night['compound'].sum()
day_sentiment = day['compound'].sum()
love_sentiment = love['compound'].sum()
hurt_sentiment = hurt['compound'].sum()

print("\nNight Sentiment: ", night_sentiment)
print("Day Sentiment: ", day_sentiment)
print("Love Sentiment: ", love_sentiment)
print("Hurt Sentiment: ", hurt_sentiment, "\n\n")