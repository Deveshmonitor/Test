"""Trello reader."""
from typing import List

from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class TrelloReader(BaseReader):
    """Trello reader. Reads data from Trello boards and cards.

    Args:
        api_key (str): Trello API key.
        api_token (str): Trello API token.
    """

    def __init__(self, api_key: str, api_token: str) -> None:
        """Initialize Trello reader."""
        self.api_key = api_key
        self.api_token = api_token

    def load_data(self, board_id: str) -> List[DocumentNode]:
        """Load data from a Trello board.

        Args:
            board_id (str): Trello board ID.
        Returns:
            List[DocumentNode]: List of documents representing Trello cards.
        """
        from trello import TrelloClient

        client = TrelloClient(api_key=self.api_key, token=self.api_token)
        board = client.get_board(board_id)
        cards = board.get_cards()

        documents = []
        for card in cards:
            doc = DocumentNode(
                doc_id=card.name,
                text=card.description,
                extra_info={
                    "id": card.id,
                    "url": card.url,
                    "due_date": card.due_date,
                    "labels": [label.name for label in card.labels],
                },
            )
            documents.append(doc)

        return documents
