from langchain_community.document_loaders import UnstructuredWordDocumentLoader


class WordDocumentLoader:
    def __init__(self, doc_path):
        self.loader = UnstructuredWordDocumentLoader(doc_path)

    def load(self):
        return self.loader.load()
