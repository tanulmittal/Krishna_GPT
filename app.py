import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import random

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

# List of Geeta shlokas
geeta_shlokas = [
    "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
    "योगस्थ: कुरु कर्माणि सङ्गं त्यक्त्वा धनंजय। सिद्ध्यसिद्ध्यो: समो भूत्वा समत्वं योग उच्यते॥",
    "बुद्धियुक्तो जहातीह उभे सुकृतदुष्कृते। तस्माद्योगाय युज्यस्व योग: कर्मसु कौशलम्॥",
    "श्रेयान्स्वधर्मो विगुण: परधर्मात्स्वनुष्ठितात्। स्वधर्मे निधनं श्रेय: परधर्मो भयावह:॥",
    "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत। अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
    "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।",
    "सञ्जय उवाच। दृष्ट्वा तु पाण्डवानीकं व्यूढं दुर्योधनस्तदा। आचार्यमुपसङ्गम्य राजा वचनमब्रवीत्।",
    "अज्ञश्चाश्रद्दधानश्च संशयात्मा विनश्यति। नायं लोकोऽस्ति न परो न सुखं संशयात्मनः।",
    "मन्मना भव मद्भक्तो मद्याजी मां नमस्कुरु। मामेवैष्यसि सत्यं ते प्रतिजाने प्रियोऽसि मे।",
    "न त्वेवाहं जातु नासं न त्वं नेमे जनाधिपाः। न चैव न भविष्यामः सर्वे वयमतः परम्।",
    "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत। अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्।",
]

# Function to get a random shloka
def get_random_shloka():
    return random.choice(geeta_shlokas)

# Streamlit app
st.title("Ask Krishna")

# Initialize chat history and shloka
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Display random shloka when user first visits
    random_shloka = get_random_shloka()
    krishna_avatar = "https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/krishna_avatar.png"
    st.session_state.messages.append({"role": "assistant", "content": f"Radhe Radhe Parth! Here's something for you:\n\n{random_shloka}", "avatar": krishna_avatar})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question, Parth"):
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
