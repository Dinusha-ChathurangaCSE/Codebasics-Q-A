import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains import SequentialChain
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
load_dotenv()

llm = ChatGoogleGenerativeAI(google_api_key=os.environ['GOOGLE_API_KEY'], model="gemini-pro", temperature=0.6)
# from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import CSVLoader


# !pip uninstall sentence-transformers
# !pip install sentence-transformers==2.2.2

from langchain_community.embeddings import HuggingFaceInstructEmbeddings
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS

instructor_embeddings = HuggingFaceInstructEmbeddings(
    model_name = "hkunlp/instructor-large",
)
vectordb_file_path= "faiss_index"

# !pip install faiss-cpu

def create_vector_db():
  loader = CSVLoader(
      file_path='codebasics_faqs.csv',
      source_column='prompt',
      encoding='cp1252'  # Ensure UTF-8 encoding for broader character support
  )
  data = loader.load()
  vectordb = FAISS.from_documents(documents = data, embedding=instructor_embeddings)
  vectordb.save_local(vectordb_file_path)
  
  
def get_qa_chain():
  vectordb = FAISS.load_local(vectordb_file_path,instructor_embeddings,allow_dangerous_deserialization=True)
  retreiver = vectordb.as_retriever()
  prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
  CONTEXT: {context}

  QUESTION: {question}"""


  PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context", "question"]
  )
  chain_type_kwargs = {"prompt": PROMPT}

  qa_chain = RetrievalQA.from_llm(
      llm=llm, retriever=retreiver, prompt = PROMPT, return_source_documents=True
  )
  return qa_chain
  
if __name__ == "__main__":
  chain= get_qa_chain()
  print(chain("do you have emi option"))