"""dad_jokes reader"""

from typing import List

import requests
from openagent.knowledgebase.document_loaders.basereader import BaseReader
from openagent.schema import DocumentNode


class DadJokesReader(BaseReader):
    """Dad jokes reader.

    Reads a random dad joke.

    """

    def _get_random_dad_joke(self):
        response = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        json_data = response.json()
        return json_data["joke"]

    def load_data(self) -> List[DocumentNode]:
        """Return a random dad joke.

        Args:
            None.

        """
        return [DocumentNode(text=self._get_random_dad_joke())]
