import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.log_wrapper import LogWrapper


def default_faiss_vector_store_wrapper(logger: LogWrapper, index_path: str, dataset_path: str):
    return FaissVectorStoreWrapper(logger=logger,
                                   azure_embeddings=AzureOpenAIEmbeddings(model="text-embedding-ada-002"),
                                   chunk_splitter=RecursiveCharacterTextSplitter(chunk_size=500,
                                                                                 chunk_overlap=20),
                                   index_path=index_path,
                                   data_set_path=str(dataset_path)).init_local_vector_store_with_data_set()


class FaissVectorStoreWrapper:
    def __init__(self, logger: LogWrapper,
                 azure_embeddings: AzureOpenAIEmbeddings,
                 chunk_splitter: RecursiveCharacterTextSplitter,
                 index_path: str,
                 data_set_path: str):

        self.logger = logger
        self.azure_embeddings = azure_embeddings
        self.chunk_splitter = chunk_splitter
        self.index_path = index_path
        self.data_set_path = data_set_path

    def init_local_vector_store_with_data_set(self) -> FAISS:
        # Currently only supports docx dataset! extend if needed
        vectorstore = None

        # 2. Check if FAISS index exists
        if os.path.exists(os.path.join(self.index_path, "index.faiss")) and \
                os.path.exists(os.path.join(self.index_path, "index.pkl")):

            # 3. Load if exists
            self.logger.info(f"Attempting to load existing FAISS index from {self.index_path}")
            try:
                vectorstore = FAISS.load_local(
                    self.index_path,
                    self.azure_embeddings,
                    # Necessary due to pickle usage by LangChain for metadata.
                    # Ensure the index files haven't been tampered with.
                    allow_dangerous_deserialization=True
                )
                self.logger.info("FAISS index loaded successfully from disk.")
            except Exception as load_err:
                self.logger.error(
                    f"Failed to load FAISS index from {self.index_path}: {load_err}. Will attempt rebuild.",
                    exc_info=True)
                vectorstore = None  # Reset on failure

        # 4. Build and Save if not loaded/exists
        if vectorstore is None:
            self.logger.info(
                f"No existing index found or loading failed. Building new FAISS index from {self.data_set_path}...")

            # --- Load and Split Documents ---
            try:
                loader = DirectoryLoader(self.data_set_path, glob="**/*.docx", show_progress=True)
                docs = loader.load()
                if not docs:
                    raise ValueError(f"No documents found in {self.data_set_path}")

                splits = self.chunk_splitter.split_documents(docs)
                if not splits:
                    raise ValueError("Document splitting resulted in no chunks.")
                self.logger.info(f"Loaded and split {len(docs)} documents into {len(splits)} chunks.")

                # --- Embed and Create Index ---
                self.logger.info("Embedding documents and building FAISS index (this may take a while)...")
                vectorstore = FAISS.from_documents(splits, self.azure_embeddings)
                self.logger.info("FAISS index built successfully.")

                # --- Save Index ---
                self.logger.info(f"Saving FAISS index to {self.index_path}...")
                os.makedirs(self.index_path, exist_ok=True)  # Ensure directory exists
                vectorstore.save_local(self.index_path)
                self.logger.info(f"FAISS index saved successfully.")

            except Exception as build_err:
                self.logger.error(f"Fatal error during FAISS index build/save: {build_err}", exc_info=True)
                # Depending on your app's requirements, you might want to raise here
                # to prevent the app starting without a vectorstore.
                raise RuntimeError(f"Could not initialize FAISS vectorstore: {build_err}")
        return vectorstore
