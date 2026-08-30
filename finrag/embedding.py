from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)


def get_embedding_model():
    """
    Trả về Embedding Model.
    """

    return embedding_model
