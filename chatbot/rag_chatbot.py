"""
RAG Chatbot Implementation using LangChain

This module implements a Retrieval Augmented Generation (RAG) chatbot that can
answer questions based on the PDF documents in the repository.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# Import knowledge graph utilities
from chatbot.knowledge_graph import load_knowledge_graph


class RAGChatbot:
    """RAG Chatbot for answering questions about PDF documents"""
    
    def __init__(
        self,
        documents_dir: str = "pdfs",
        vector_store_dir: str = ".chroma_db",
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
    ):
        """
        Initialize the RAG chatbot.
        
        Args:
            documents_dir: Directory containing the documents
            vector_store_dir: Directory to store the vector database
            model_name: Name of the LLM model to use
            temperature: Temperature for response generation
        """
        load_dotenv()
        
        self.documents_dir = Path(documents_dir)
        self.vector_store_dir = vector_store_dir
        self.model_name = model_name
        self.temperature = temperature
        
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature
        )
        self.vector_store: Optional[Chroma] = None
        self.qa_chain = None
        self.knowledge_graph = None
        
        print(f"RAG Chatbot initialized with model: {self.model_name}")
    
    def load_documents(self) -> List:
        """Load all documents from the documents directory"""
        print(f"Loading documents from {self.documents_dir}...")
        
        if not self.documents_dir.exists():
            raise FileNotFoundError(f"Documents directory not found: {self.documents_dir}")
        
        # Load text files (we're using .txt files as PDF placeholders)
        loader = DirectoryLoader(
            str(self.documents_dir),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        
        documents = loader.load()
        print(f"Loaded {len(documents)} documents")
        
        return documents
    
    def split_documents(self, documents: List) -> List:
        """Split documents into chunks for processing"""
        chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        
        return chunks
    
    def create_vector_store(self, documents: List) -> Chroma:
        """Create or load vector store from documents"""
        print("Creating vector store...")
        
        # Create vector store
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.vector_store_dir
        )
        
        print(f"Vector store created with {len(documents)} chunks")
        return vector_store
    
    def load_vector_store(self) -> Optional[Chroma]:
        """Load existing vector store"""
        if Path(self.vector_store_dir).exists():
            print("Loading existing vector store...")
            try:
                vector_store = Chroma(
                    persist_directory=self.vector_store_dir,
                    embedding_function=self.embeddings
                )
                return vector_store
            except Exception as e:
                print(f"Error loading vector store: {e}")
                return None
        return None
    
    def setup(self, force_rebuild: bool = False):
        """Set up the chatbot by loading/creating vector store and QA chain"""
        print("Setting up RAG chatbot...")
        
        # Load knowledge graph if available
        self.knowledge_graph = load_knowledge_graph()
        if self.knowledge_graph:
            print(self.knowledge_graph.get_graph_summary())
        
        # Load or create vector store
        if not force_rebuild:
            self.vector_store = self.load_vector_store()
        
        if self.vector_store is None:
            documents = self.load_documents()
            chunks = self.split_documents(documents)
            self.vector_store = self.create_vector_store(chunks)
        
        # Create custom prompt template
        template = """You are a helpful AI assistant that answers questions based on the provided context from technical documents about machine learning, data science, and programming.

Use the following pieces of context to answer the question at the end. If you don't know the answer or if the context doesn't contain the information, say so honestly. Don't make up information.

When answering:
1. Be concise but comprehensive
2. Cite which document or topic the information comes from when possible
3. If the question requires information from multiple documents, synthesize the information
4. Use technical terms appropriately

Context:
{context}

Question: {question}

Answer: """

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create conversational retrieval chain
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT}
        )
        
        print("RAG chatbot setup complete!")
    
    def query(self, question: str) -> Dict:
        """
        Query the chatbot with a question.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary containing the answer and source documents
        """
        if self.qa_chain is None:
            raise RuntimeError("Chatbot not set up. Call setup() first.")
        
        print(f"\n🤔 Question: {question}")
        
        result = self.qa_chain({"question": question})
        
        answer = result["answer"]
        sources = result.get("source_documents", [])
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def format_response(self, result: Dict) -> str:
        """Format the response with sources"""
        answer = result["answer"]
        sources = result["sources"]
        
        response = f"\n💡 Answer:\n{answer}\n"
        
        if sources:
            response += f"\n📚 Sources:\n"
            seen_sources = set()
            for i, doc in enumerate(sources, 1):
                source = doc.metadata.get("source", "Unknown")
                source_name = Path(source).stem
                if source_name not in seen_sources:
                    seen_sources.add(source_name)
                    response += f"  {i}. {source_name}\n"
        
        return response
    
    def chat_loop(self):
        """Run interactive chat loop"""
        print("\n" + "="*60)
        print("🤖 RAG Chatbot - Ready to answer your questions!")
        print("="*60)
        print("\nAsk questions about:")
        print("  - Machine Learning")
        print("  - Natural Language Processing")
        print("  - Deep Learning")
        print("  - Data Science")
        print("  - Python Programming")
        print("\nCommands:")
        print("  'exit' or 'quit' - Exit the chatbot")
        print("  'docs' - List available documents")
        print("  'graph' - Show knowledge graph summary")
        print("="*60 + "\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if question.lower() == 'docs':
                    if self.knowledge_graph:
                        docs = self.knowledge_graph.get_documents()
                        print(f"\n📄 Available documents ({len(docs)}):")
                        for doc in docs:
                            info = self.knowledge_graph.get_document_info(doc)
                            if info:
                                print(f"  - {doc} ({info.get('word_count', 0)} words)")
                    else:
                        print("\n📄 Documents in pdfs/:")
                        for f in self.documents_dir.glob("*.txt"):
                            print(f"  - {f.stem}")
                    print()
                    continue
                
                if question.lower() == 'graph':
                    if self.knowledge_graph:
                        print(f"\n{self.knowledge_graph.get_graph_summary()}")
                    else:
                        print("\n⚠️  Knowledge graph not available")
                    print()
                    continue
                
                result = self.query(question)
                print(self.format_response(result))
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue


def main():
    """Main entry point for the chatbot"""
    try:
        # Initialize chatbot
        chatbot = RAGChatbot()
        
        # Setup (will use cached vector store if available)
        chatbot.setup()
        
        # Start interactive chat
        chatbot.chat_loop()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
