import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# Set up OpenAI API key
api_key = st.secrets["openai_api_key"]

# Read the prompt from prompt.txt
with open("prompt.txt", "r") as file:
    gita_prompt = file.read().strip()

# Set up LangChain components
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=api_key, streaming=True)

# Create a ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(
    f"{gita_prompt}\n\nConversation history: {{chat_history}}\nHuman: {{user_question}}\nKrishna:"
)

# Create the chain
chain = prompt_template | llm | StrOutputParser()

# Function to generate streaming response
def get_response(user_query, chat_history):
    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

# Streamlit app
st.title("Ask Krishna")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question, Parth:"):
    # Display user message in chat message container
    user_avatar = "https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/user_avatar.png"
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": user_avatar})

    # Generate streaming response
    chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    krishna_avatar = "https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/krishna_avatar.png"
    with st.chat_message("assistant", avatar=krishna_avatar):
        response = st.write_stream(get_response(prompt, chat_history))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": krishna_avatar})
