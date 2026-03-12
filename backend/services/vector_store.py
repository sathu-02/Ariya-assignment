from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from openai import OpenAI
from config import settings
import uuid


class VectorStore:
    """
    Qdrant Vector Database service.

    Responsibilities:
    - create collection
    - embed text
    - store vectors
    - retrieve relevant context
    """

    def __init__(self):

        # Qdrant client
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )

        # OpenAI client
        self.openai = OpenAI(api_key=settings.OPENAI_API_KEY)

        self.collection_name = "career_knowledge"

        # Create the collection on initialization if it doesn't exist
        try:
            self.create_collection()
        except Exception:
            pass

    # ---------------------------------------------------
    # Create collection
    # ---------------------------------------------------

    def create_collection(self):

        collections = self.client.get_collections().collections
        existing = [c.name for c in collections]

        if self.collection_name in existing:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

    # ---------------------------------------------------
    # Generate embeddings
    # ---------------------------------------------------

    def embed(self, text: str) -> List[float]:

        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    # ---------------------------------------------------
    # Insert knowledge documents
    # ---------------------------------------------------

    def add_documents(self, documents: List[str]):

        points = []

        for doc in documents:

            vector = self.embed(doc)

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={"text": doc}
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    # ---------------------------------------------------
    # Semantic search
    # ---------------------------------------------------

    def search(self, query: str, limit: int = 3) -> List[str]:

        vector = self.embed(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit
        )

        docs = []

        for r in results:
            docs.append(r.payload["text"])

        return docs