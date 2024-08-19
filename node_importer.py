import csv
from neo4j import GraphDatabase

class NodeImporter:
    """
    A class to import nodes into a Cypher (Neo4j) database.

    Attributes:
        driver: Neo4j driver to interact with the database.
    """

    def __init__(self, uri, user, password, database):
        """Initialize the NodeImporter with Neo4j connection details."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the Neo4j driver connection."""
        self.driver.close()

    def create_node(self, label, properties):
        """
        Create a node in the database.

        Args:
            label (str): The label for the node.
            properties (dict): A dictionary of properties for the node.
        """
        with self.driver.session() as session:
            properties["uuid"] = session.run("RETURN apoc.create.uuid() AS uuid").single()["uuid"]
            query = f"CREATE (n:{label} {{ {', '.join(f'{k}: ${k}' for k in properties)} }})"
            session.run(query, **properties)

    def import_nodes_from_csv(self, file_path, label, property_mapping):
        """
        Import nodes from a CSV file into the database.

        Args:
            file_path (str): Path to the CSV file.
            label (str): Label for the nodes.
            property_mapping (dict): Mapping of CSV columns to node properties and data types.
        """
        with open(file_path, mode='r') as file:
            reader = csv.reader(file, skipinitialspace=True, quotechar='"', delimiter=',', escapechar='\\')
            for row in reader:
                properties = {}
                for csv_column in property_mapping:
                    col = list(csv_column.keys())[0]
                    data_type = csv_column[col][1]
                    propname = csv_column[col][0]
                    # print(list(csv_column.keys())[0])
                    properties[propname] = self.cast_type(row[int(col)], data_type)
                self.create_node(label, properties)

    @staticmethod
    def cast_type(value, data_type):
        """
        Cast a string value to a specified data type.

        Args:
            value (str): The value to cast.
            data_type (type): The data type to cast to.

        Returns:
            The value cast to the specified data type.
        """
        if data_type == 'int':
            return int(value)
        elif data_type == 'float':
            return float(value)
        elif data_type == 'bool':
            return value.lower() in ("yes", "true", "1")
        return value  # Default to str
