#Code taken from langchain Github Repo and removed load method as it involved Documents from langchain

"""Util that calls Wikipedia."""
import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

logger = logging.getLogger(__name__)

WIKIPEDIA_MAX_QUERY_LENGTH = 300


class WikipediaAPIWrapper(BaseModel):
    """Wrapper around WikipediaAPI.

    To use, you should have the ``wikipedia`` python package installed.
    This wrapper will use the Wikipedia API to conduct searches and
    fetch page summaries. By default, it will return the page summaries
    of the top-k results.
    It limits the Document content by doc_content_chars_max.
    """

    wiki_client: Any  #: :meta private:
    top_k_results: int = 3
    lang: str = "en"
    load_all_available_meta: bool = False
    doc_content_chars_max: int = 4000

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the python package exists in environment."""
        try:
            import wikipedia

            wikipedia.set_lang(values["lang"])
            values["wiki_client"] = wikipedia
        except ImportError:
            raise ImportError(
                "Could not import wikipedia python package. "
                "Please install it with `pip install wikipedia`."
            )
        return values

    def run(self, query: str) -> str:
        """Run Wikipedia search and get page summaries."""
        page_titles = self.wiki_client.search(query[:WIKIPEDIA_MAX_QUERY_LENGTH])
        summaries = []
        for page_title in page_titles[: self.top_k_results]:
            if wiki_page := self._fetch_page(page_title):
                if summary := self._formatted_page_summary(page_title, wiki_page):
                    summaries.append(summary)
        if not summaries:
            return "No good Wikipedia Search Result was found"
        return "\n\n".join(summaries)[: self.doc_content_chars_max]

    @staticmethod
    def _formatted_page_summary(page_title: str, wiki_page: Any) -> Optional[str]:
        return f"Page: {page_title}\nSummary: {wiki_page.summary}"


    def _fetch_page(self, page: str) -> Optional[str]:
        try:
            return self.wiki_client.page(title=page, auto_suggest=False)
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            return None