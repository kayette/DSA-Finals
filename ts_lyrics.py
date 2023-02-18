# inspired by https://github.com/irenetrampoline/taylor-swift-lyrics/blob/master/scrape.py 
# and https://www.youtube.com/watch?v=KjhqAiJNLnQ

from bs4 import BeautifulSoup
import requests
import random

link = requests.get('https://www.azlyrics.com/t/taylorswift.html')
soup = BeautifulSoup(link.text, 'lxml')
songs = soup.find_all(class_ = 'listalbum-item')
urls = []

for song in songs:
    urls.append(song.find('a'))

for i in range(len(urls)):
    if i != 180:
        urls[i]['href'] = 'https://www.azlyrics.com' + urls[i]['href']

which_song = random.choice(urls)['href']
soup = BeautifulSoup(requests.get(which_song).text, 'lxml')
lyrics = soup.find(class_ = 'col-xs-12 col-lg-8 text-center')
lyrics = lyrics.text.strip()
lyrics = lyrics[lyrics.find('\n\n\n\n')+5: lyrics.find('Submit Corrections')]
lyrics = lyrics.splitlines()
a = []

for i in range(len(lyrics)):
    if lyrics[i] == '':
        a.append(i)

for num in a:
    lyrics.remove('')

lyrics.pop()
song_name = lyrics[0]
lyrics.remove(song_name)

def generate_lyrics():
    x = random.randint(0, len(lyrics)-2)
    print("\n\nHere are your lyrics!")
    print('\n' + lyrics[x] + '\n' + lyrics[x+1] + " (" + song_name + ")" + '\n')

def word_counter():
    search_word_count = input("\nEnter the word: ")
    file = open("lyrics.txt", encoding="utf8")
    read_data = file.read()
    word_count = read_data.lower().count(search_word_count)
    print(f"\nThe word '{search_word_count}' appeared in Taylor Swift's lyrics a total of: {word_count} times.")

while True:
    print("\n===================================================\nWhat would you like to do?\n")
    print("1 - Random Lyrics Generator")
    print("2 - Word Counter")
    print("3 - Quit")

    user_input = input("\nEnter your destination: ")

    if user_input == "1":
        generate_lyrics()
    elif user_input == "2":
        word_counter()
    elif user_input == "3":
        print("\nThank you for using this program!\n")
        break
    else:
        print("===================================================\nInvalid Input\nPlease Try Again.\n")