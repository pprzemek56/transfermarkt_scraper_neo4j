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
    print(fetch_all_clubs(leagues_links[0]))


def fetch_all_clubs(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_tags = soup.findAll('td', class_='hauptlink no-border-links')
    football_teams = {}
    for td_tag in td_tags:
        a_tag = td_tag.find('a')
        football_teams.update({a_tag.get('title'): 'https://www.transfermarkt.com' + a_tag.get('href')})
    return football_teams


if __name__ == '__main__':
    main()
