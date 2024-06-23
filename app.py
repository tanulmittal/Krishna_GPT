import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from PIL import Image

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

# Load images
user_image = Image.open("user_avatar.png")
krishna_image = Image.open("krishna_avatar.png")

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

st.markdown("""
<style>
    [data-testid="chatAvatarIcon-user"] svg {
        display: none;
    }
    [data-testid="chatAvatarIcon-user"]::after {
        content: url('https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/user_avatar.png');
        display: inline-block;
        width: 32px;
        height: 32px;
    }
    [data-testid="chatAvatarIcon-assistant"] svg {
        display: none;
    }
    [data-testid="chatAvatarIcon-assistant"]::after {
        content: url('https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/krishna_avatar.png');
        display: inline-block;
        width: 32px;
        height: 32px;
    }
</style>
""", unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question, Parth"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate streaming response
    chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    with st.chat_message("assistant"):
        response = st.write_stream(get_response(prompt, chat_history))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
