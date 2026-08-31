def create_retriever(vector_store):
    """
    Tạo Retriever từ Vector Store.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={
           
            "k": 3
        }
    )

    return retriever