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

    # fetch all league nodes
    leagues = conn.fetch_nodes('League')

    for league in leagues:
        league_soup = get_soup(league['n.url'])
        clubs = fetch_all_clubs(league_soup)

        # create club nodes and relationship with league
        for club in clubs:
            # create club node
            conn.create_club(club)
            # fetch club and create a relationship with league where it belongs
            club_node = conn.fetch_club_by_name(club.get('name'))
            conn.create_belong_relationship(league['n.name'], club_node[0]['n.name'])

    # fetch all clubs
    clubs = conn.fetch_nodes('Club')

    for club in clubs:
        club_soup = get_soup(club['n.url'])

        # scrape all players from giving club
        players = fetch_all_players(club_soup)
        for player in players:
            player_soup = get_soup(player.get('url'))
            previous_clubs = fetch_all_previous_clubs(player_soup, club['n.name'])

            # create node player
            conn.create_player(player)

            # fetch player and create a relationship with club where he plays
            player_node = conn.fetch_player_by_name(player.get('name'))
            conn.create_playing_relationship(club['n.name'], player_node[0]['n.name'])

            # create relationship with clubs where player played before
            for previous_club in previous_clubs:
                previous_club_node = conn.fetch_club_by_name(previous_club)
                if previous_club_node:
                    conn.create_played_relationship(previous_club_node[0]['n.name'],
                                                    player_node[0]['n.name'])


def get_soup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')


def fetch_all_previous_clubs(soup, current_club):
    # player soup needed
    previous_clubs = []
    for club in soup.find_all('a', class_='tm-player-transfer-history-grid__club-link'):
        club_name = club.get_text(strip=True)
        if club_name != current_club and club_name not in previous_clubs:
            previous_clubs.append(club_name)
    return previous_clubs


def fetch_all_clubs(soup):
    # league soup needed
    td_tags = soup.findAll('td', class_='hauptlink no-border-links')
    football_teams = []
    for td_tag in td_tags:
        a_tag = td_tag.find('a')
        football_teams.append({'name': a_tag.get('title'), 'url': ULR_PREFIX + a_tag.get('href')})
    return football_teams


def get_league(soup, url):
    # league soup needed
    name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald') \
        .get_text(strip=True)
    nationality = soup.find('span', class_='data-header__club').find('a').get_text(strip=True)
    return {'name': name, 'nationality': nationality, 'url': url}


def fetch_all_players(soup):
    # club soup needed
    table_tag = soup.findAll('table', class_='inline-table')
    players = []
    for table in table_tag:
        a_tag = table.find('span', class_='hide-for-small').find('a')
        players.append({'name': a_tag.get_text(strip=True), 'url': ULR_PREFIX + a_tag.get('href')})
    return players


if __name__ == '__main__':
    main()
