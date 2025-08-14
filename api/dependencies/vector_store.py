from langchain_community.vectorstores import FAISS

from fastapi import Request


def get_vector_store_dependency(
        request: Request,
) -> FAISS:
    context = request.app.state.context
    return context.get("book_recommendation_faiss")
