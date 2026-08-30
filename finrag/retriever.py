def create_retriever(vector_store):
    """
    Tạo Retriever từ Vector Store.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={
            #Tăng số dòng truy xuất từ 3 lên 6 để tra cứu đúng hơn 363636
            "k": 6
        }
    )

    return retriever
