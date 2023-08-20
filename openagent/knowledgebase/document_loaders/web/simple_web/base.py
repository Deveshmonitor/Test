"""Simple Web scraper."""
from typing import List

from langchain.requests import RequestsWrapper
from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class SimpleWebPageReader(BaseReader):
    """Simple web page reader.

    Reads pages from the web.

    Args:
        html_to_text (bool): Whether to convert HTML to text.
            Requires `html2text` package.

    """

    def __init__(self, html_to_text: bool = False) -> None:
        """Initialize with parameters."""
        self._html_to_text = html_to_text

    def load_data(self, urls: List[str]) -> List[DocumentNode]:
        """Load data from the input directory.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[DocumentNode]: List of documents.

        """
        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        requests = RequestsWrapper()
        documents = []
        for url in urls:
            response = requests.get(url)
            if self._html_to_text:
                import html2text

                response = html2text.html2text(response)
            metadata = {"url": url}
            documents.append(DocumentNode(text=response, extra_info=metadata))

        return documents
