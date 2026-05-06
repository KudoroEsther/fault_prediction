import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from powerbot.app.utils.helpers import ensure_directory


logger = logging.getLogger(__name__)


def create_embeddings(api_key: str, model: str = "text-embedding-3-small") -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=model, openai_api_key=api_key)


def _get_client(persist_directory: Path) -> chromadb.PersistentClient:
    ensure_directory(persist_directory)
    return chromadb.PersistentClient(
        path=str(persist_directory),
        settings=ChromaSettings(allow_reset=True),
    )


def load_vectorstore(
    embeddings: OpenAIEmbeddings,
    persist_directory: Path,
    collection_name: str = "agentic_fault_docs",
) -> Chroma:
    client = _get_client(persist_directory)
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )


def create_vectorstore(
    chunks: list[Document],
    embeddings: OpenAIEmbeddings,
    persist_directory: Path,
    collection_name: str = "agentic_fault_docs",
) -> Chroma:
    vectorstore = load_vectorstore(
        embeddings=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
    if not chunks:
        return vectorstore

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [chunk.metadata["chunk_id"] for chunk in chunks]
    vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    logger.info("Stored %s RAG chunks in Chroma", len(chunks))
    return vectorstore
