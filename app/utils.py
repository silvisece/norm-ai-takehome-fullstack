
from pydantic import BaseModel, Field
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI
from llama_index.schema import Document
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
)
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
import os
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

class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

class DocumentMetadata(BaseModel):
    level_id: str = Field(..., description="The identifier of the level (e.g., '6.11.1')")
    section_id: str = Field(..., description="The highest level section identifier (e.g., '6')")
    # section_title: Optional[str] = Field(None, description="The title of the section (e.g., 'Thievery')")
    # source_file: str = Field(..., description="Source document name")
    title: str = Field(..., description="Document title")
    # page_number: Optional[int] = Field(None, description="Page number in the source document")
    parsed_at: date = Field(default_factory=date.today, description="Date document was parsed")


class DocumentService(BaseModel):
    file_path: str

    @staticmethod
    def chunk_text(text: str, has_title: bool = True) -> tuple[list[dict], str]:
        """
        Splits `text` into chunks, each chunk containing:
            {
            "heading": <the heading line>,
            "text": <subsequent lines until the next heading, joined by spaces>
            }
        A line is considered a heading if it matches either:
        - numeric_heading_pattern (like "1.2.")
        - word_colon_pattern (like "Citations:")
        
        Arguments:
            text: str - The text to chunk
            has_title: bool - Whether the text has a title line
        Returns: 
            tuple[list[dict], str] - A tuple containing:
                list[dict] - A list of chunks, each chunk containing a heading and the subsequent text
                title: str - The title of the document
        """
        title = None
        # Assumptions about header format
        numeric_heading_pattern = re.compile(r'^[0-9]+(?:\.[0-9]+)*\.$')
        word_colon_pattern = re.compile(r'^[A-Za-z]+:$', re.IGNORECASE)

        def _is_new_heading(line: str) -> bool:
            """
            Returns True if the line matches either:
            - A numeric heading like "1.1."
            - A single word followed by a colon (e.g. "Citations:", "References:")
            """
            stripped = line.strip()
            if numeric_heading_pattern.match(stripped):
                return True
            if word_colon_pattern.match(stripped):
                return True
            return False

        lines = text.splitlines()
        chunks = []
        current_heading = None
        current_body = []

        # Assumption: first line title 
        start_index = 0 
        if has_title:
            start_index = 1
            title = lines[0]    
        
        for line in lines[start_index:]:
            if _is_new_heading(line):
                # Finalize the previous chunk if we have one
                if current_heading is not None:
                    joined_text = " ".join(current_body).strip()
                    chunks.append({
                        "heading": current_heading,
                        "text": joined_text
                    })
                    current_body = []
                # Start a new heading
                current_heading = line.strip()
            else:
                # Accumulate lines for the current chunk
                current_body.append(line.strip())

        # Finalize the last chunk
        if current_heading is not None:
            joined_text = " ".join(current_body).strip()
            chunks.append({
                "heading": current_heading,
                "text": joined_text
            })

        return chunks, title

    def create_documents(self) -> list[Document]:
        """
        Enrich chunk metadata and output a list of Document objects.
        """
        
        with open(self.file_path, 'r') as file:
            text = file.read()
        
        docs = []
        chunks, title = self.chunk_text(text, has_title=True)
        # add metadata to each chunk
        for chunk in chunks:
            metadata = DocumentMetadata(
                level_id=chunk['heading'],
                section_id=chunk['heading'].split('.')[0],
                title=title,
                parsed_at=datetime.now().date()
            )

            docs.append(Document(
                metadata=metadata.model_dump(),
                text=chunk['text']
            ))

        return docs

class QdrantService:
    def __init__(self, k: int = 2):
        self.index = None
        self.k = k

    def connect(self) -> None:
        client = qdrant_client.QdrantClient(location=":memory:")

        vstore = QdrantVectorStore(client=client, collection_name='temp')

        service_context = ServiceContext.from_defaults(
            embed_model=OpenAIEmbedding(),
            llm=OpenAI(api_key=key, model="gpt-4o")
            )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore, 
            service_context=service_context
            )

    def load(self, docs = list[Document]):
        self.index.insert_nodes(docs)

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


if __name__ == "__main__":
    # Example workflow
    doc_serivce = DocumentService() # implemented
    docs = doc_serivce.create_documents() # NOT implemented

    index = QdrantService() # implemented
    index.connect() # implemented
    index.load() # implemented

    index.query("what happens if I steal?") # NOT implemented
