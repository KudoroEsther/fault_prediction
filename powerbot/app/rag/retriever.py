import logging
from functools import lru_cache
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from powerbot.app.core.config import get_settings
from powerbot.app.rag.vector_store import create_embeddings, create_vectorstore, load_vectorstore


logger = logging.getLogger(__name__)


def load_and_chunk_documents(
    data_path: Path,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[Document]:
    if not data_path.exists() or not data_path.is_dir():
        return []

    loaders = {
        ".txt": lambda path: TextLoader(str(path), encoding="utf-8"),
        ".pdf": lambda path: PyPDFLoader(str(path)),
    }

    documents: list[Document] = []
    for file_path in data_path.iterdir():
        if not file_path.is_file():
            continue
        loader_factory = loaders.get(file_path.suffix.lower())
        if not loader_factory:
            continue
        try:
            documents.extend(loader_factory(file_path).load())
        except Exception as exc:
            logger.warning("Unable to load %s: %s", file_path.name, exc)

    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    for index, chunk in enumerate(chunks):
        chunk.metadata.update(
            {
                "chunk_id": f"chunk_{index}",
                "chunk_index": index,
                "source_file": Path(chunk.metadata.get("source", "unknown")).name,
            }
        )
        chunk.metadata = {
            key: value if isinstance(value, (str, int, float, bool)) else str(value)
            for key, value in chunk.metadata.items()
        }
    return chunks


@lru_cache(maxsize=1)
def get_vectorstore():
    settings = get_settings()
    api_key = settings.resolved_openai_api_key
    if not api_key:
        raise RuntimeError("OpenAI API key is not configured.")

    embeddings = create_embeddings(api_key)
    vectorstore = load_vectorstore(
        embeddings=embeddings,
        persist_directory=settings.vectorstore_dir,
    )

    try:
        collection = vectorstore.get()
        if collection.get("ids"):
            return vectorstore
    except Exception:
        logger.info("No existing vectorstore collection found, attempting bootstrap.")

    chunks = load_and_chunk_documents(settings.rag_docs_dir)
    if not chunks:
        logger.warning("No RAG documents available in %s", settings.rag_docs_dir)
        return vectorstore
    return create_vectorstore(
        chunks=chunks,
        embeddings=embeddings,
        persist_directory=settings.vectorstore_dir,
    )


def retrieve_documents(query: str, k: int = 4) -> str:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": max(k * 2, 8)},
    )
    documents = retriever.invoke(query)
    if not documents:
        return "No relevant documents found."

    return "\n\n---\n\n".join(
        f"Document {index + 1}:\n{document.page_content}"
        for index, document in enumerate(documents)
    )
