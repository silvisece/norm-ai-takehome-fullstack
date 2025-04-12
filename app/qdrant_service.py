from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.query_engine import CitationQueryEngine
from dataclasses import dataclass
import os
import yaml
import re

key = os.environ['OPENAI_API_KEY']


@dataclass
class Input:
    query: str
    file_path: str

@dataclass
class Citation:
    source: str
    text: str
    score: str

class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

    def __str__(self):
        return (f"Query: {self.query}\n"
                f"Response: {self.response}\n"
                f"Citations: {self.citations}")

class QdrantService:
    def __init__(self, k: int = 5):
        self.index = None
        self.k = k

        with open("app/config.yml", 'r') as file:
            config = yaml.safe_load(file)

        Settings.llm = OpenAI(model=config['llm_model'])
        Settings.embed_model = OpenAIEmbedding(model=config['embed_model'])

    def connect(self, docs = list[Document]) -> None:
        client = qdrant_client.QdrantClient(location=":memory:")

        vector_store = QdrantVectorStore(
            client=client, 
            collection_name='medieval_laws',
        )
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context
        )

    def load(self, docs = list[Document]) -> None:
        parser = SimpleNodeParser()
        nodes = parser.get_nodes_from_documents(docs)
        self.index.insert_nodes(nodes)

    # def load(self, docs: list[Document]) -> None:
    #     self.index = VectorStoreIndex.from_documents(docs)

    def query(self, query_str: str) -> Output:
        """
        This method needs to initialize the query engine, run the query, and return
        the result as a pydantic Output class. This is what will be returned as
        JSON via the FastAPI endpount. 
        worth noting:llama-index package has a CitationQueryEngine...

        Also, be sure to make use of self.k (the number of vectors to return based
        on semantic similarity).

        # Example output object
        citations = [
            Citation(source="Law 1", text="Theft is punishable by hanging"),
            Citation(source="Law 2", text="Tax evasion is punishable by banishment."),
        ]

        output = Output(
            query=query_str, 
            response=response_text, 
            citations=citations
            )

        return output

        """
        query_engine = CitationQueryEngine.from_args(
            index=self.index,
            similarity_top_k=self.k
        )
        response = query_engine.query(query_str)
        source_nodes = response.source_nodes

        # Process citations
        citations = []
        for i, node_with_score in enumerate(source_nodes, start=1):
            node = node_with_score.node
            score = str(round(node_with_score.score, 2))
            metadata = node.metadata
            source = f"[{i}] {metadata.get('title')} - {metadata.get('level_id')}"
            text = node.get_text()
            text = re.sub(r'^Source \d+:\s*', '', text) # Remove "Source #:" pattern 
            citations.append(Citation(source=source, text=text, score=score))

        # Get citation indices from response, reindex
        citation_indices = sorted(set(int(match) for match in re.findall(r'\[(\d+)\]', str(response))))
        filtered_citations = [citations[i - 1] for i in citation_indices if 1 <= i <= len(citations)]

        # Create the Output object
        output = Output(
            query=query_str,
            response=str(response),
            citations=filtered_citations
        )

        return output
