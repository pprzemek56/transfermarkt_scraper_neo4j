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
    get_player(get_soup(https://www.transfermarkt.com/alex-meret/profil/spieler/240414))


def get_soup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')


def fetch_all_clubs(soup):
    # league url needed
    td_tags = soup.findAll('td', class_='hauptlink no-border-links')
    football_teams = []
    for td_tag in td_tags:
        a_tag = td_tag.find('a')
        football_teams.append({'name': a_tag.get('title'), 'url': ULR_PREFIX + a_tag.get('href')})
    return football_teams


def get_league(soup):
    # league url needed
    name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald') \
        .text.strip()
    nationality = soup.find('span', class_='data-header__club').find('a').text.strip()
    is_top_5 = nationality in top_5_leagues
    return {'name': name, 'nationality': nationality, 'is_top_5': is_top_5}


def get_club(soup):
    # club url needed
    name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald') \
        .text.strip()
    league = soup.find('span', class_='data-header__club').find('a').text.strip()
    return {'name': name, 'league': league}


def fetch_all_players(soup):
    # club url needed
    table_tag = soup.findAll('table', class_='inline-table')
    players = []
    for table in table_tag:
        a_tag = table.find('span', class_='hide-for-small').find('a')
        players.append({'name': a_tag.text.strip(), 'url': ULR_PREFIX + a_tag.get('href')})
    return players


def get_league_url(soap):
    # club url needed
    return ULR_PREFIX + soap.find('span', 'data-header__club').find('a').get('href')


def get_player(soap):
    # player url needed
    print(soap.find('span', 'data-header__shirt-number'))


if __name__ == '__main__':
    main()
