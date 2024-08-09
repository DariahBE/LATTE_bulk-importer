import yaml
from node_importer.py import NodeImporter
from edge_importer.py import EdgeImporter

class ImportTool:
    """
    A class to manage the importing of nodes and edges into a Cypher (Neo4j) database.

    Attributes:
        config (dict): Configuration data loaded from the YAML file.
        node_importer (NodeImporter): Instance of NodeImporter for importing nodes.
        edge_importer (EdgeImporter): Instance of EdgeImporter for importing edges.
    """

    def __init__(self, config_path, db_uri, db_user, db_password):
        """Initialize the ImportTool with the configuration file and Neo4j connection details."""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.node_importer = NodeImporter(db_uri, db_user, db_password)
        self.edge_importer = EdgeImporter(db_uri, db_user, db_password)

    def import_data(self):
        """Import nodes and edges according to the configuration file."""
        for node_config in self.config.get('nodes', []):
            self.node_importer.import_nodes_from_csv(
                file_path=node_config['file'],
                label=node_config['label'],
                property_mapping=node_config['properties']
            )

        for edge_config in self.config.get('edges', []):
            self.edge_importer.import_edges_from_csv(
                file_path=edge_config['file'],
                start_label=edge_config['start_label'],
                end_label=edge_config['end_label'],
                relationship=edge_config['relationship'],
                start_id_column=edge_config['start_id'],
                end_id_column=edge_config['end_id']
            )

    def close(self):
        """Close the connections to the Neo4j database."""
        self.node_importer.close()
        self.edge_importer.close()

if __name__ == "__main__":
    config_path = 'config.yaml'
    #todo: read from YAML 
    db_uri = "bolt://localhost:7687"
    db_user = "neo4j"
    db_password = "your_password"

    tool = ImportTool(config_path, db_uri, db_user, db_password)
    try:
        tool.import_data()
    finally:
        tool.close()
