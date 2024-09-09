import csv
from neo4j import GraphDatabase

class EdgeImporter:
    """
    A class to import edges into a Cypher (Neo4j) database.

    Attributes:
        driver: Neo4j driver to interact with the database.
    """

    def __init__(self, uri, user, password, databases):
        """Initialize the EdgeImporter with Neo4j connection details."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def create_edge(self, start_label, start_id, end_label, end_id, relationship):
        """
        Create an edge between two nodes in the database.

        Args:
            start_label (str): Label of the starting node.
            end_label (str): Label of the ending node.
            start_id (str): ID of the starting node.
            end_id (str): ID of the ending node.
            relationship (str): Relationship type.
        """
        with self.driver.session() as session:
            query = f"""
            MATCH (a) where a.{start_label} = $start_id
            MATCH (b) where b.{end_label} = $end_id
            CREATE (a)-[r:{relationship}]->(b)
            """
            session.run(query, start_id=start_id, end_id=end_id)

    def import_edges_from_csv(self, file_path, edge_props):
        """
        Import edges from a CSV file into the database.

        Args:
            file_path (str): Path to the CSV file.
            edge_props = dict with the YAML defined properties for the nodes. 
        """
        #EDGE properties are tripples: StartID, stopID, edgelabel!
        #We only need the properties to get the user chosen names for start- and stop id
        startlabel = edge_props[0][0][0]
        stoplabel = edge_props[1][1][0]
        with open(file_path, mode='r') as file:
            reader = csv.reader(file, delimiter=',', escapechar='\\',quotechar='"', skipinitialspace=True)
            for row in reader:
                self.create_edge(startlabel, int(row[0]), stoplabel, int(row[1]), row[2])
