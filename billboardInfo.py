import requests
from bs4 import BeautifulSoup

base_url = "https://www.billboard.com/charts/hot-100/"


class BillboardInfo:
    def __init__(self):
        self.date = self.get_date()
        self.url = f"{base_url}{self.date}"

    def getTitles(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        songs = soup.find_all(name="li", class_="o-chart-results-list__item")
        titles = []

        for song in songs:
            song_title = song.find(name="h3")
            if song_title:
                titles.append(song_title.text.strip())
        return titles

    @staticmethod
    def get_date():
        answer = input("what date you would like to travel to? (YYYY-MM-DD) ")
        return answer
