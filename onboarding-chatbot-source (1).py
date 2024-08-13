# onboarding_chatbot.py

import os
import faiss
import numpy as np
from typing import List
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize LangChain components
llm = OpenAI(temperature=0.7)
embeddings = OpenAIEmbeddings()

# Define database schema
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_number = Column(String)
    email = Column(String, unique=True)
    business_name = Column(String)
    business_type = Column(String)
    company_size = Column(String)
    company_location = Column(String)
    company_website = Column(String)

# Onboarding questions
onboarding_questions = [
    {"id": 1, "question": "What is your full name?", "field": "name"},
    {"id": 2, "question": "What is your contact number?", "field": "contact_number"},
    {"id": 3, "question": "What is your email address?", "field": "email"},
    {"id": 4, "question": "What is your business name?", "field": "business_name"},
    {"id": 5, "question": "What type of business do you run?", "field": "business_type"},
    {"id": 6, "question": "How many employees does your company have?", "field": "company_size"},
    {"id": 7, "question": "Where is your company located?", "field": "company_location"},
    {"id": 8, "question": "What is your company's website?", "field": "company_website"}
]

# Load and prepare the knowledge base
def load_knowledge_base(directory: str) -> List[str]:
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(directory, filename))
            documents.extend(loader.load())
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    return texts

# Create FAISS index
def create_faiss_index(texts: List[str]) -> FAISS:
    return FAISS.from_documents(texts, embeddings)

# Set up RAG
def setup_rag(index: FAISS) -> RetrievalQA:
    retriever = index.as_retriever(search_kwargs={"k": 2})
    return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Initialize database
engine = create_engine('sqlite:///onboarding.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Load knowledge base and create index
knowledge_base_dir = "path/to/your/knowledge_base"
texts = load_knowledge_base(knowledge_base_dir)
faiss_index = create_faiss_index(texts)

# Set up RAG
rag = setup_rag(faiss_index)

# Onboarding conversation
def onboarding_conversation():
    template = """
    You are an AI assistant helping with user onboarding. Ask the user the following question:
    {question}
    Current conversation:
    {chat_history}
    Human: {human_input}
    AI: """

    prompt = PromptTemplate(
        input_variables=["question", "chat_history", "human_input"],
        template=template
    )

    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )

    chat_history = []

    print("Welcome to the onboarding process!")
    for question in onboarding_questions:
        while True:
            response = conversation.predict(question=question['question'], chat_history="\n".join(chat_history), human_input="")
            print(f"AI: {response}")
            user_input = input("Human: ").strip()
            
            if user_input.lower() == "help":
                help_response = rag.run(f"Provide more information about {question['field']}")
                print(f"AI: {help_response}")
            elif user_input.lower() == "done":
                store_response(question['field'], user_input)
                chat_history.append(f"Human: {user_input}")
                chat_history.append(f"AI: Thank you. Let's move on to the next question.")
                break
            else:
                store_response(question['field'], user_input)
                chat_history.append(f"Human: {user_input}")
                chat_history.append(f"AI: Thank you for providing that information.")
                break

    print("Onboarding process completed. Do you have any other questions?")
    while True:
        user_input = input("Human: ").strip()
        if user_input.lower() == "exit":
            break
        response = rag.run(user_input)
        print(f"AI: {response}")

def store_response(field, value):
    user = session.query(User).first()
    if not user:
        user = User()
        session.add(user)
    setattr(user, field, value)
    session.commit()

if __name__ == "__main__":
    onboarding_conversation()
