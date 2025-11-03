#!/usr/bin/env python
# coding: utf-8

# In[1]:


from langchain_core.documents import Document


# In[6]:


doc = Document(
    page_content="Hii here theh rag_demo working...........",
    metadata= {
        "source" : "web",
        "pages" : 1,
        "data of created" : "2026-10-30",
        "Author" : "MaskMan"


    }
)
doc


# In[7]:


import os

os.makedirs("../data/text_files", exist_ok=True)


# In[37]:


sample_texts= {
    "../data/text_files/python_intro.txt" : """Python is a high-level, interpreted, general-purpose programming language. Created by Guido van Rossum and first released in 1991, it is known for its emphasis on code readability and its use of significant indentation. The name "Python" was inspired by the British comedy series Monty Python's Flying Circus. 
Key Characteristics and Features:
Readability: Python's syntax is designed to be clear and concise, often described as English-like, making it easier to learn and understand compared to many other languages.
Interpreted: Python code does not need to be compiled before execution. An interpreter runs the code directly, allowing for rapid development and testing.
Dynamically Typed: Variable types are determined at runtime, meaning you don't need to explicitly declare the type of a variable when you create it.
High-Level Language: Python abstracts away many low-level details of computer hardware, allowing developers to focus on higher-level problem-solving.
Multiple Programming Paradigms: It supports various programming styles, including object-oriented, imperative, and functional programming.
Extensive Standard Library: Python comes with a large collection of modules and packages that provide pre-written code for a wide range of tasks, reducing the need to write everything from scratch.
Cross-Platform Compatibility: Python can run on various operating systems, including Windows, macOS, and Linux, without requiring significant code changes.
Free and Open-Source: Python is freely available for use and distribution, and its source code is open for modification and improvement by a global community.
Common Applications:
Python is widely used in diverse fields, including:
Web Development: Frameworks like Django and Flask facilitate building web applications.
Data Science and Machine Learning: Libraries such as NumPy, Pandas, Scikit-learn, TensorFlow, and PyTorch are essential for data analysis, visualization, and building machine learning models.
Automation and Scripting: Its simplicity makes it ideal for automating repetitive tasks and system administration.
Software Development: Used for building desktop applications and integrating with other systems.
Artificial Intelligence: A popular choice for developing AI algorithms and applications."""
}



for path, content in sample_texts.items():
    with open(path, 'w', encoding="utf-8") as f:
        f.write(content)
print("txt created sucessfully......!")



# In[ ]:


sample_texts= {
    "../data/text_files/rag_introtxt" : """Retrieval-Augmented Generation (RAG) is an artificial intelligence (AI) framework that improves large language models (LLMs) by giving them access to up-to-date, external data sources. This process makes LLM-generated responses more accurate, context-specific, and reliable than those produced by the model's original, static training data alone. 
How RAG works
A RAG system follows a series of steps to generate a response for a user query: 
Ingestion: A knowledge base, which can contain a variety of data types like PDFs, databases, and websites, is created. An embedding model converts this data into numerical representations, called vectors, and stores them in a vector database.
Retrieval: When a user submits a query, the system uses a retriever model to search the vector database for the most relevant information.
Augmentation: The retrieved, contextual information is added to the user's original query to create an enhanced prompt.
Generation: The augmented prompt is sent to the large language model, which uses both its initial training data and the newly retrieved information to create a final, well-grounded response. 
Key benefits of using RAG
Reduces "hallucinations": Since RAG grounds responses in factual, external data, it significantly lowers the risk of the LLM presenting false or nonsensical information.
Provides up-to-date information: RAG systems can be updated continuously with fresh information without the need for expensive and time-consuming model retraining.
Adds domain-specific knowledge: Companies can connect LLMs to their own internal documents, product manuals, or policies, enabling them to produce more specialized and relevant answers.
Builds user trust: RAG allows the model to cite its sources, giving users the ability to verify the information for themselves.
Increases cost efficiency: Organizations can improve the performance of a foundational model for specific tasks by using RAG, which is far less expensive than fine-tuning or retraining the entire LLM. 
Common RAG applications
Customer service chatbots: A chatbot can provide specific, up-to-date information by referencing a company's internal knowledge base and product manuals.
Research assistants: RAG can help financial analysts, medical professionals, and other researchers quickly access and synthesize information from vast databases of records, journals, and reports.
Internal knowledge management: Employees can query an organization's documents using conversational language to find actionable insights, streamline onboarding, or get HR support.
Content generation: The technology can be used to gather information from multiple authoritative sources and generate more reliable articles or summaries. 
"""
}



for path, content in sample_texts.items():
    with open(path, 'w', encoding="utf-8") as f:
        f.write(content)
print("txt created sucessfully......!")



# In[8]:


from langchain_community.document_loaders import TextLoader

loader = TextLoader("../data/text_files/python_intro.txt", encoding="utf-8")

document = loader.load()
print(document)


# In[9]:


from langchain_community.document_loaders import DirectoryLoader

dir_loader = DirectoryLoader(
    "../data/text_files",
    glob="**/*.txt",
    loader_cls=TextLoader,
    show_progress=False

)
documents = dir_loader.load()
documents


# In[10]:


from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader

my_dir = DirectoryLoader(
    "../data/pdf",
    glob="**/*.pdf",
    loader_cls= PyMuPDFLoader,
    show_progress= False

)
dir_documents = my_dir.load()
dir_documents


# In[12]:


type(dir_documents[0])


# ### Embedding Part
# 

# In[17]:


import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Any, Tuple, Dict
from sklearn.metrics.pairwise import cosine_similarity



# In[24]:


class EmbeddingManager:
    def __init__(self, model_name : str = "all-MiniLM-L6-v2"):
        self.model_name = model_name 
        self.model = None
        self._load_model()


    def _load_model(self):
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"model loaded Sucessfully. Embedding dimension.{self.model.get_sentence_embedding_dimension()}")
        except Exception as e: 
            print(f"Error loading model {self.model_name}: {e}")
            raise
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model not loaded")
        
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings
 
embedding_manager=EmbeddingManager()
embedding_manager





# In[28]:


import os
class VectorStore:
    """Manages document embeddings in a ChromaDB vector store"""
    
    def __init__(self, collection_name: str = "pdf_documents", persist_directory: str = "../data/vector_store"):
        """
        Initialize the vector store
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the vector store
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Create persistent ChromaDB client
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "PDF document embeddings for RAG"}
            )
            print(f"Vector store initialized. Collection: {self.collection_name}")
            print(f"Existing documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise

    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        """
        Add documents and their embeddings to the vector store
        
        Args:
            documents: List of LangChain documents
            embeddings: Corresponding embeddings for the documents
        """
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        print(f"Adding {len(documents)} documents to vector store...")
        
        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            # Generate unique ID
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            # Prepare metadata
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            
            # Document content
            documents_text.append(doc.page_content)
            
            # Embedding
            embeddings_list.append(embedding.tolist())
        
        # Add to collection
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text
            )
            print(f"Successfully added {len(documents)} documents to vector store")
            print(f"Total documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

vectorstore=VectorStore()
vectorstore
    


# In[ ]:




