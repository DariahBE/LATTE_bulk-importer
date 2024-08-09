import csv
from neo4j import GraphDatabase

class EdgeImporter:
    """
    A class to import edges into a Cypher (Neo4j) database.

    Attributes:
        driver: Neo4j driver to interact with the database.
    """

    def __init__(self, uri, user, password):
        """Initialize the EdgeImporter with Neo4j connection details."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def create_edge(self, start_label, end_label, start_id, end_id, relationship):
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
            MATCH (a:{start_label} {{id: $start_id}})
            MATCH (b:{end_label} {{id: $end_id}})
            CREATE (a)-[r:{relationship}]->(b)
            """
            session.run(query, start_id=start_id, end_id=end_id)

    def import_edges_from_csv(self, file_path, start_label, end_label, relationship, start_id_column, end_id_column):
        """
        Import edges from a CSV file into the database.

        Args:
            file_path (str): Path to the CSV file.
            start_label (str): Label of the starting node.
            end_label (str): Label of the ending node.
            relationship (str): Relationship type.
            start_id_column (str): CSV column name for start node IDs.
            end_id_column (str): CSV column name for end node IDs.
        """
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.create_edge(start_label, end_label, row[start_id_column], row[end_id_column], relationship)
