from __future__ import annotations

from app.core.config import settings
from app.vectorstore.chroma.chroma_client import get_chroma_client


def get_threats_collection():
    """
    Collection containing known attack prompt signatures (seed dataset + curated).
    """

    client = get_chroma_client()
    return client.get_or_create_collection(name=settings.CHROMA_COLLECTION_THREATS)


def get_mutations_collection():
    """
    Collection containing adversarially mutated variants of known attacks.
    """

    client = get_chroma_client()
    return client.get_or_create_collection(name=settings.CHROMA_COLLECTION_MUTATIONS)

