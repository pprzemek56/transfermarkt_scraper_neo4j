import requests
from bs4 import BeautifulSoup

from database import conn

ULR_PREFIX = 'https://www.transfermarkt.com'

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

top_5_leagues = ['Italy', 'England', 'Spain', 'France', 'Germany']


def main():
    print(get_club({'name': 'SSC Napoli', 'url': 'https://www.transfermarkt.com/ssc-neapel/startseite/verein/6195/saison_id/2022'}))


def fetch_all_clubs(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_tags = soup.findAll('td', class_='hauptlink no-border-links')
    football_teams = {}
    for td_tag in td_tags:
        a_tag = td_tag.find('a')
        football_teams.update({'name': a_tag.get('title'), 'url': ULR_PREFIX + a_tag.get('href')})
    return football_teams


def get_league(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tag = soup.find('span', class_='data-header__club').find('a')
    league = {'name': a_tag.text.strip(), 'url': ULR_PREFIX + a_tag.get('href')}

    response = requests.get(league['url'], headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tag = soup.find('span', class_='data-header__club').find('a')
    league.pop('url', None)
    league.update({'nationality': a_tag.text.strip()})
    league.update({'is_top_5': a_tag.text.strip() in top_5_leagues})
    return league


def get_club(club):
    response = requests.get(club.get('url'), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    club = {'name': club.get('name')}
    a_tag = soup.find('span', class_='data-header__club').find('a')
    club.update({'league': a_tag.text.strip()})
    return club


if __name__ == '__main__':
    main()
