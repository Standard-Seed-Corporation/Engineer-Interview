"""
Knowledge Graph Utilities
Load and interact with the knowledge graph created by the GitHub Actions workflow.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set
import networkx as nx


class KnowledgeGraphLoader:
    """Load and query the knowledge graph"""
    
    def __init__(self, graph_path: str = "knowledge_graph.json"):
        """
        Initialize the knowledge graph loader.
        
        Args:
            graph_path: Path to the knowledge graph JSON file
        """
        self.graph_path = Path(graph_path)
        self.graph_data: Optional[Dict] = None
        self.nx_graph: Optional[nx.Graph] = None
        
    def load(self) -> bool:
        """
        Load the knowledge graph from JSON file.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not self.graph_path.exists():
                print(f"Warning: Knowledge graph not found at {self.graph_path}")
                return False
                
            with open(self.graph_path, 'r') as f:
                self.graph_data = json.load(f)
            
            # Rebuild NetworkX graph
            self.nx_graph = nx.Graph()
            
            for node in self.graph_data.get('nodes', []):
                node_id = node['id']
                self.nx_graph.add_node(node_id, **{k: v for k, v in node.items() if k != 'id'})
            
            for edge in self.graph_data.get('edges', []):
                source = edge['source']
                target = edge['target']
                edge_data = {k: v for k, v in edge.items() if k not in ['source', 'target']}
                self.nx_graph.add_edge(source, target, **edge_data)
            
            print(f"Loaded knowledge graph with {len(self.graph_data['nodes'])} nodes and {len(self.graph_data['edges'])} edges")
            return True
            
        except Exception as e:
            print(f"Error loading knowledge graph: {e}")
            return False
    
    def get_documents(self) -> List[str]:
        """Get list of all document names in the knowledge graph"""
        if not self.graph_data:
            return []
        return list(self.graph_data.get('documents', {}).keys())
    
    def get_document_info(self, doc_name: str) -> Optional[Dict]:
        """Get information about a specific document"""
        if not self.graph_data:
            return None
        return self.graph_data.get('documents', {}).get(doc_name)
    
    def get_related_documents(self, doc_name: str) -> List[str]:
        """Get documents related to the given document"""
        if not self.nx_graph or doc_name not in self.nx_graph:
            return []
        
        related = []
        for neighbor in self.nx_graph.neighbors(doc_name):
            node_data = self.nx_graph.nodes[neighbor]
            if node_data.get('type') == 'document':
                related.append(neighbor)
        
        return related
    
    def get_document_topics(self, doc_name: str) -> List[str]:
        """Get topics associated with a document"""
        doc_info = self.get_document_info(doc_name)
        if doc_info:
            return doc_info.get('topics', [])
        return []
    
    def get_documents_by_topic(self, topic: str) -> List[str]:
        """Find documents that discuss a specific topic"""
        if not self.graph_data:
            return []
        
        matching_docs = []
        for doc_name, doc_info in self.graph_data.get('documents', {}).items():
            topics = [t.lower() for t in doc_info.get('topics', [])]
            if topic.lower() in topics:
                matching_docs.append(doc_name)
        
        return matching_docs
    
    def search_topics(self, query: str) -> List[str]:
        """Search for topics matching a query string"""
        if not self.graph_data:
            return []
        
        query_lower = query.lower()
        matching_topics = set()
        
        for doc_info in self.graph_data.get('documents', {}).values():
            for topic in doc_info.get('topics', []):
                if query_lower in topic.lower():
                    matching_topics.add(topic)
        
        return sorted(list(matching_topics))
    
    def get_statistics(self) -> Dict:
        """Get knowledge graph statistics"""
        if not self.graph_data:
            return {}
        return self.graph_data.get('statistics', {})
    
    def get_graph_summary(self) -> str:
        """Get a human-readable summary of the knowledge graph"""
        if not self.graph_data:
            return "Knowledge graph not loaded"
        
        stats = self.get_statistics()
        documents = self.get_documents()
        
        summary = f"""Knowledge Graph Summary:
- Total Documents: {stats.get('total_documents', 0)}
- Total Nodes: {stats.get('total_nodes', 0)}
- Total Edges: {stats.get('total_edges', 0)}

Documents:
"""
        for doc in documents:
            doc_info = self.get_document_info(doc)
            if doc_info:
                summary += f"  - {doc}: {doc_info.get('word_count', 0)} words, {len(doc_info.get('topics', []))} topics\n"
        
        return summary


def load_knowledge_graph(graph_path: str = "knowledge_graph.json") -> Optional[KnowledgeGraphLoader]:
    """
    Convenience function to load the knowledge graph.
    
    Args:
        graph_path: Path to the knowledge graph JSON file
        
    Returns:
        KnowledgeGraphLoader instance if successful, None otherwise
    """
    loader = KnowledgeGraphLoader(graph_path)
    if loader.load():
        return loader
    return None
