import json
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class JSONLoader(BaseLoader):
    def __init__(
        self,
        file_path: Union[str, Path],
        content_key: Optional[str] = None,
        ):
        self.file_path = Path(file_path).resolve()
        self._content_key = content_key
        
    def load(self) -> List[Document]:
        """Load and return documents from the JSON file."""

        docs=[]
        # Load JSON file
        with open(self.file_path) as file:
            data = json.load(file)

            # Iterate through 'pages'
            for page in data['pages']:
                parenturl = page['parenturl']
                pagetitle = page['pagetitle']
                indexeddate = page['indexeddate']
                snippets = page['snippets']

                # Process snippets for each page
                for snippet in snippets:
                    index = snippet['index']
                    childurl = snippet['childurl']
                    text = snippet['text']
                    metadata = dict(
                        source=childurl,
                        title=pagetitle)

                    docs.append(Document(page_content=text, metadata=metadata))
        return docs

