from typing import List
from ctx.app_context import AppContext


def embed_query(ctx: AppContext, query: str) -> List[float]:
    embeddings_client = ctx.get("embeddings_client")
    return embeddings_client.embed_query(query)
