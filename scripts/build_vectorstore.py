from powerbot.app.core.config import get_settings
from powerbot.app.rag.retriever import load_and_chunk_documents
from powerbot.app.rag.vector_store import create_embeddings, create_vectorstore


def build_vectorstore() -> None:
    settings = get_settings()
    api_key = settings.resolved_openai_api_key
    if not api_key:
        raise RuntimeError("OpenAI API key is not configured.")

    chunks = load_and_chunk_documents(settings.rag_docs_dir)
    embeddings = create_embeddings(api_key)
    create_vectorstore(
        chunks=chunks,
        embeddings=embeddings,
        persist_directory=settings.vectorstore_dir,
    )
    print(f"Vectorstore built at {settings.vectorstore_dir}")


if __name__ == "__main__":
    build_vectorstore()
