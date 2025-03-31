from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv, find_dotenv

# Cargar variables de entorno
_ = load_dotenv(find_dotenv())
groq_api_key = os.environ["GROQ_API_KEY"]

# Cargar PDF
loader = PyPDFLoader("./rey_invierno.pdf")
docs = loader.load()

# Dividir en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Crear vectorstore
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=splits, embedding=embedding)

# Crear retriever
retriever = vectorstore.as_retriever()

# Cargar prompt desde LangChain Hub
prompt = hub.pull("rlm/rag-prompt")

# Instanciar el LLM (Groq)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Función para formatear los documentos recuperados
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Crear la cadena RAG
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Usar el pipeline
pregunta = "Explicame con detalle como son las reglas de combate?"
respuesta = rag_chain.invoke(pregunta)
print(respuesta)