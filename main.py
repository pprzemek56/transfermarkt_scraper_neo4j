import re
import requests
from bs4 import BeautifulSoup

from database import Neo4jConnection

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
    # create connection
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="password")

    for link in leagues_links:
        league_soup = get_soup(link)
        league = get_league(league_soup, link)

        # create league node
        conn.create_league('league', league)

    # select all league nodes
    leagues = conn.fetch_nodes('League')
    for league in leagues:
        league_soup = get_soup(league['n.url'])
        clubs_url = fetch_all_clubs(league_soup)








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


def get_league(soup, url):
    # league url needed
    name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald') \
        .get_text(strip=True)
    nationality = soup.find('span', class_='data-header__club').find('a').get_text(strip=True)
    return {'name': name, 'nationality': nationality, 'url': url}


def get_club(soup):
    # club url needed
    if not soup.find('div', class_='data-header__box--big'):
        return None

    name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald') \
        .get_text(strip=True)
    league = soup.find('span', class_='data-header__club').find('a').get_text(strip=True)
    return {'name': name, 'league': league}


def fetch_all_players(soup):
    # club url needed
    table_tag = soup.findAll('table', class_='inline-table')
    players = []
    for table in table_tag:
        a_tag = table.find('span', class_='hide-for-small').find('a')
        players.append({'name': a_tag.get_text(strip=True), 'url': ULR_PREFIX + a_tag.get('href')})
    return players


def get_league_url(soup):
    # club url needed
    return ULR_PREFIX + soup.find('span', 'data-header__club').find('a').get('href')


def get_player_and_fetch_all_previous_clubs(soup):
    # player url needed
    headline = soup.find('h1', class_='data-header__headline-wrapper')
    text = ' '.join(headline.text.split())
    try:
        name, surname = re.sub(r'#\d{1,2}', '', text).strip().split(maxsplit=1)
    except ValueError:
        surname = re.sub(r'#\d{1,2}', '', text).strip()
        name = ''

    current_club = soup.find('span', class_='data-header__club').get_text(strip=True)
    transfers = soup.findAll('div', class_='grid tm-player-transfer-history-grid')
    previous_clubs = []
    for transfer in transfers:
        grid_cell = transfer.find('div',
                                  class_='grid__cell grid__cell--center tm-player-transfer-history-grid__old-club')
        try:
            link = ULR_PREFIX + grid_cell.find('a', class_='tm-player-transfer-history-grid__club-link').get('href')
        except AttributeError:
            continue

        club_soup = get_soup(link)
        club = get_club(club_soup)
        if club is None or club.get('name') == current_club or club in previous_clubs:
            continue
        previous_clubs.append(club)

    return {'name': name,
            'surname': surname,
            'current_club': current_club,
            'previous_clubs': previous_clubs}


if __name__ == '__main__':
    main()
