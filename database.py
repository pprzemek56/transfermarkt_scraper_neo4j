from neo4j import GraphDatabase


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e, 'query = ', query)
        finally:
            if session is not None:
                session.close()
        return response

    def create_league(self, label, properties):
        query = f'MERGE (n:League {{name: "{properties["name"]}",' \
                f' nationality: "{properties["nationality"]}",' \
                f' url: "{properties["url"]}"}})'
        self.query(query)

    def create_club(self, properties):
        query = f"""
        MERGE (n:Club {{name: "{properties['name']}", url: "{properties['url']}"}})
        """
        self.query(query)

    def create_player(self, properties):
        query = f"""
        MERGE (n:Player {{name: "{properties['name']}", url: "{properties['url']}"}})
        """
        self.query(query)

    def fetch_nodes(self, label):
        query = f'MATCH (n:{label}) RETURN ID(n), n.name, n.nationality, n.url'
        return self.query(query)

    def fetch_club_by_name(self, club_name):
        club_name = club_name.replace("'", "\\'")
        query = f"MATCH (n:Club) WHERE n.name = '{club_name}' RETURN ID(n), n.name, n.url"
        return self.query(query)

    def fetch_player_by_name(self, player_name):
        player_name = player_name.replace("'", "\\'")
        query = f"MATCH (n:Player) WHERE n.name = '{player_name}' RETURN ID(n), n.name, n.url"
        return self.query(query)

    def create_belong_relationship(self, league_name, club_name):
        query = f"""
            MATCH (l:League {{name: '{league_name}'}}), (c:Club {{name: '{club_name}'}})
            MERGE (c)-[r:BELONGS_TO]->(l)
            """
        self.query(query)

    def create_playing_relationship(self, club_name, player_name):
        club_name = club_name.replace("'", "\\'")
        player_name = player_name.replace("'", "\\'")
        query = f"""
            MATCH (c:Club {{name: '{club_name}'}}), (p:Player {{name: '{player_name}'}})
            MERGE (p)-[r:PLAYING]->(c)
            """
        self.query(query)

    def create_played_relationship(self, club_name, player_name):
        club_name = club_name.replace("'", "\\'")
        player_name = player_name.replace("'", "\\'")
        query = f"""
            MATCH (c:Club {{name: '{club_name}'}}), (p:Player {{name: '{player_name}'}})
            MERGE (p)-[r:PLAYED]->(c)
            """
        self.query(query)


conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="password")
