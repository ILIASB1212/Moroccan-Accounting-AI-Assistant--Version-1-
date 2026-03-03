

from src.data_ingestion.documents_loader import DocumentLoader
from src.data_ingestion.embedding import  Embeddings
from src.data_ingestion.text_spliter import TextSpliter
from src.data_ingestion.vectorestore import VectorStore
from pathlib import Path
class RagPipeLine:
    def __init__(self,data_dir,persist_dir,force_rebuild,chunk_size,chunk_overlap):
        self.data_dir=data_dir
        self.persist_dir=persist_dir
        self.force_rebuild=force_rebuild
        self.chunk_size=chunk_size
        self.chunk_overlap=chunk_overlap
        self.vectorstore = None  # Initialize as None
        self.retriever = None

        persist_path = Path(self.persist_dir)
        self.vectorstore_exists = (persist_path.exists() and 
                            any(persist_path.glob("*.sqlite3")))  # Chroma files

        print(f"\n{'='*50}")
        print(f"🚀 RAG Pipeline initialized")
        print(f"📂 Data: {self.data_dir}")
        print(f"💾 Persist: {self.persist_dir}")
        print(f"🔍 Vectorstore exists: {self.vectorstore_exists}")
        print(f"{'='*50}\n")
    def run(self):
        embeddings_model=Embeddings()
        embedings=embeddings_model.initializing_embedding()
        self.vectordatabase =VectorStore(embeddings=embedings,
                                persist_directory=self.persist_dir)
        if self.vectorstore_exists and not self.force_rebuild:
            print("🔄 Loading existing vectorstore...")
            self.vectorstore=self.vectordatabase.load_existing() 
            print(f"✅ Loaded existing vectorstore from {self.persist_dir}")

        else:
            document_loader=DocumentLoader(directory=self.data_dir,extract_images=False)
            text_spliter=TextSpliter(chunk_size=self.chunk_size,chunk_overlap=self.chunk_overlap)

            documents=document_loader.document_loader()
            print(f"📄 Loaded {len(documents)} documents from cgnc folder")
            if not documents:
                print("❌ No documents to process. Please add PDF files to data/CGNC/")
                raise ValueError(f"❌ No documents found in {self.data_dir}")
            print("🔤 Embeddings ready")
            chunks =text_spliter.split_documents(documents)
            if not chunks:
                print("❌ No chunks created. Check your PDF files.")
                raise ValueError("❌ No chunks created. Check your PDF files.")
                
            db = self.vectordatabase.create_from_documents(chunks)
            print(f"💾 Vectorstore created with {len(chunks)} documents from cgnc ")
        self.retriever=self.vectordatabase.get_retriever()
        print(f"✅ retriver for {self.persist_dir} is ready to use ")
        return self.retriever

                
                



