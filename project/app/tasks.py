from bs4 import BeautifulSoup
import requests
from app.models import Genre, Song

response = requests.get('https://muz-tv.ru/music/playlist/top50/')
soup = BeautifulSoup(response.text, 'html.parser')
song_genre = soup.find_all('div', class_="title-h2 title-trans-no")
song_name = soup.find_all('div', class_="info")

def parse_song() -> None:
    for genre, name in zip(song_genre, song_name):
        my_genre = genre.get_text(strip=True)
        my_name = name.get_text(strip=True)
        genres = Genre.objects.create(genre=my_genre)
        Song.objects.create(name=my_name, genre=genres)