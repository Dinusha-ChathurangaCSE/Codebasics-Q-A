# import streamlit as st 
# from langchain_helper import create_vector_db,get_qa_chain

# st.title("Codebasics QA 🌿 ")
# btn = st.button("Create knowledge base")

# if btn:
#   pass

# question  = st.text_input("Question: ")

# if question:
#   chain = get_qa_chain()
#   response = chain(question)
  
#   st.header("Answer: ")
#   st.write(response["result"])
import streamlit as st
from langchain_helper import get_qa_chain

# Initialize or load conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # A list to store the conversation history
if "question" not in st.session_state:
    st.session_state.question = ""

st.title("Codebasics QA 🌿 ")
btn = st.button("Create knowledge base")

if btn:
    pass  # Add your knowledge base creation logic here
  
# Button to clear the conversation history
clear_history_btn = st.button("Clear Conversation History")

if clear_history_btn:
    st.session_state.conversation = [] 
    
# Input for the user's question
def clear_input():
    st.session_state.widget = ""
# Input for the user's question
question = st.text_input("Question:",value=st.session_state.question)
st.session_state.question = "" 
if question:
    # Get the chain and response from the QA model
    chain = get_qa_chain()
    response = chain(question)
    
    # Append the new question and response to the conversation history
    st.session_state.conversation.append({"question": question, "answer": response["result"]})
    
    # Clear the question field after the response
    clear_input() 
    
# Display the conversation history
st.header("Conversation History:")

for i, entry in enumerate(st.session_state.conversation):
    st.write(f"**Question {i+1}:** {entry['question']}")
    st.write(f"**Answer {i+1}:** {entry['answer']}")
