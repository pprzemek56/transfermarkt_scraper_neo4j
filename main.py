import requests
from bs4 import BeautifulSoup

from database import conn

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
}

leagues_links = [
    'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
    'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1',
    'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
    'https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1',
    'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1'
]


def main():
    fetch_all_clubs()


def fetch_all_clubs():
    for link in leagues_links:
        response = requests.get(leagues_links[0], headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.find(class_='hauptlink no-border-links'))


if __name__ == '__main__':
    main()
