import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import random
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import date, datetime

# Set up OpenAI API key
api_key = st.secrets["openai_api_key"]

# Set up OpenAI client
client = OpenAI(api_key=api_key)

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

# Function to determine sun sign based on date of birth
def get_sun_sign(dob):
    month = dob.month
    day = dob.day
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "aquarius"
    else:
        return "pisces"

# Function to get horoscope
def get_horoscope(sun_sign):
    horoscope_urls = {
        "gemini": "https://www.elle.com/horoscopes/daily/a99/gemini-daily-horoscope/",
        "taurus": "https://www.elle.com/horoscopes/daily/a98/taurus-daily-horoscope/",
        "aries": "https://www.elle.com/horoscopes/daily/a60/aries-daily-horoscope/",
        "pisces": "https://www.elle.com/horoscopes/daily/a108/pisces-daily-horoscope/",
        "aquarius": "https://www.elle.com/horoscopes/daily/a107/aquarius-daily-horoscope/",
        "libra": "https://www.elle.com/horoscopes/daily/a103/libra-daily-horoscope/",
        "virgo": "https://www.elle.com/horoscopes/daily/a102/virgo-daily-horoscope/",
        "leo": "https://www.elle.com/horoscopes/daily/a101/leo-daily-horoscope/",
        "cancer": "https://www.elle.com/horoscopes/daily/a100/cancer-daily-horoscope/",
        "capricorn": "https://www.elle.com/horoscopes/daily/a106/capricorn-daily-horoscope/",
        "sagittarius": "https://www.elle.com/horoscopes/daily/a105/sagittarius-daily-horoscope/",
        "scorpio": "https://www.elle.com/horoscopes/daily/a104/scorpio-daily-horoscope/"
    }
    
    url = horoscope_urls.get(sun_sign.lower())
    if not url:
        return f"Invalid sun sign: {sun_sign}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    horoscope_content = soup.find('div', class_='article-body-content')
    
    if horoscope_content:
        paragraphs = horoscope_content.find_all('p')
        if paragraphs:
            horoscope_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
            horoscope_text = horoscope_text.replace("See All Signs", "").strip()
            return horoscope_text
    
    return f"Horoscope content not found for {sun_sign}."

# Function to rephrase horoscope
def rephrase_with_gpt(text, name):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rephrases text in simple English."},
            {"role": "user", "content": f"Rephrase the following horoscope in simple English, keep tone calm and address me with Parth, and explain me like i am an 12 year old: {text}"}
        ]
    )
    return response.choices[0].message.content.strip()

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

# Get the current year
current_year = date.today().year

# Horoscope input form
st.sidebar.header("Get Your Horoscope")
name = st.sidebar.text_input("Name")
dob = st.sidebar.date_input("Date of Birth", 
                            min_value=date(1920, 1, 1), 
                            max_value=date(current_year, 12, 31))
location = st.sidebar.text_input("Location")
birth_time = st.sidebar.time_input("Time of Birth (approx)")

if st.sidebar.button("Get Horoscope"):
    sun_sign = get_sun_sign(dob)
    horoscope = get_horoscope(sun_sign)
    rephrased_horoscope = rephrase_with_gpt(horoscope, name)
    
    krishna_avatar = "https://raw.githubusercontent.com/tanulmittal/Krishna_GPT/main/krishna_avatar.png"
    with st.chat_message("assistant", avatar=krishna_avatar):
        st.markdown(f"Here's your daily horoscope, \n\n{rephrased_horoscope}")
    
    st.session_state.messages.append({"role": "assistant", "content": f"\n\n{rephrased_horoscope}", "avatar": krishna_avatar})

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

# Add background music player
st.sidebar.markdown("---")  # Add a separator
st.sidebar.subheader("Background Music")
audio_file = open("MusicBG.mp3", "rb")
st.sidebar.audio(audio_file, format="audio/mp3")
