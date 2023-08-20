from typing import Any, List, Optional

from openagent.schema import BaseRetriever, Document


class MetalRetriever(BaseRetriever):
    def __init__(self, client: Any, params: Optional[dict] = None):
        try: 
            from metal_sdk.metal import Metal
        except ImportError:
            raise ImportError("Could not import Metal package. Please install it with 'pip install metal'")

        if not isinstance(client, Metal):
            raise ValueError(
                "Got unexpected client, should be of type metal_sdk.metal.Metal. "
                f"Instead, got {type(client)}"
            )
        self.client: Metal = client
        self.params = params or {}

    def get_relevant_documents(self, query: str) -> List[Document]:
        results = self.client.search({"text": query}, **self.params)
        final_results = []
        for r in results["data"]:
            metadata = {k: v for k, v in r.items() if k != "text"}
            final_results.append(Document(page_content=r["text"], metadata=metadata))
        return final_results

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        raise NotImplementedError("Metal retriever does not support async")