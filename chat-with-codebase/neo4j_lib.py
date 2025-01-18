from neo4j import GraphDatabase
import json

class Neo4jLoader:
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, tx, node_type, properties):
        """
        Create a node of the specified type with given properties.
        """
        query1 = f"""
        CREATE (n:{node_type} {{name: $name, path: $path, parent_name: $parent_name, 
                                parent_type: $parent_type, code: $code, docstring: $docstring}})
        """
        query = f"""
        MERGE (n:{node_type} {{name: $name, path: $path}})
        ON CREATE SET n.parent_name = $parent_name, n.parent_type = $parent_type, 
                      n.code = $code, n.docstring = $docstring, n.code_summary = $code_summary
        ON MATCH SET n.parent_name = $parent_name, n.parent_type = $parent_type, 
                     n.code = $code, n.docstring = $docstring, n.code_summary = $code_summary
        """
        tx.run(query, **properties)

    def create_relationship(self, tx, parent_type, parent_name, child_type, child_name):
        """
        Create a relationship between the parent node and the child node.
        """
        query = f"""
        MATCH (parent:{parent_type} {{name: $parent_name}})
        MATCH (child:{child_type} {{name: $child_name}})
        MERGE (parent)-[:CONTAINS]->(child)
        """
        tx.run(query, parent_name=parent_name, child_name=child_name)

    def load_data(self, data):
        """
        Load data into Neo4j.
        """
        with self.driver.session() as session:
            for item in data:
                path = item.get('path', None)
                if path is None: 
                    print(f"Skipping node with missing path: {item}")
                    continue
                # Create the current node
                properties = {
                    "name": item['name'],
                    "path": item.get('path', None),
                    "parent_name": item['parent_name'],
                    "parent_type": item['parent_type'],
                    "code": item.get('code', None),
                    "code_summary": item.get('code_summary', None),
                    "docstring": item.get('docstring', None)
                }
                session.write_transaction(self.create_node, item['type'], properties)
                # Create relationship to the parent node
                if item['parent_name']:
                    session.write_transaction(self.create_relationship, item['parent_type'], item['parent_name'], item['type'], item['name'])
        return "Nodes and Edges created successfully"


