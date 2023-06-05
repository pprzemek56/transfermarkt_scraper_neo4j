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
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

    def create_node(self, label, properties):
        query = f'CREATE (n:{label}, {properties}'
        self.query(query)

    def create_relationship(self, node1, node2, relationship_type, properties=None):
        properties = properties or {}
        query = f"MATCH (a:{node1['label']}), (b:{node2['label']}) WHERE a.id = {node1['id']} AND b.id = {node2['id']} CREATE (a)-[r:{relationship_type} {properties}]->(b)"
        self.query(query)



conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="password")
