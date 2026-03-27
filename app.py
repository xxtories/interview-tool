from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Streamlit Chat", page_icon="💬")
st.title("Chatbot")

st.subheader('Personal information', divider='rainbow')

name = st.text_input(label = "Name", max_chars = None, placeholder = "Enter your name")

experience = st.text_area(label = "Expirience", value = "", height = None, max_chars = None, placeholder = "Describe your experience")

skills = st.text_area(label = "Skills", value = "", height = None, max_chars = None, placeholder = "List your skills")

# Test labels for personal information
st.write(f"**Your Name**: {name}")
st.write(f"**Your Experience**: {experience}")
st.write(f"**Your Skills**: {skills}")

# Company and Position Section
st.subheader('Company and Position', divider = 'rainbow')

#Field for selecting the job level, position and company
col1, col2 = st.columns(2)
with col1:
    level = st.radio(
    "Choose level",
    key="visibility",
    options=["Junior", "Mid-level", "Senior"],
    )

with col2:
    position = st.selectbox(
    "Choose a position",
    ("Data Scientist", "Data engineer", "ML Engineer", "BI Analyst", "Financial Analyst"))

company = st.selectbox(
    "Choose a Company",
    ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
)

# Test labels for company and position information
st.write(f"**Your information**: {level} {position} at {company}")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful tool that speaks like a pirate"}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Your answer."):
    # Appending the user's input to the 'messages' list in session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user's message in a chat bubble
    with st.chat_message("user"):
        st.markdown(prompt)
   
    # Assistant's response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True, # This line enables streaming for real-time response
        )
        # Display the assistant's response as it streams
        response = st.write_stream(stream)
     # Append the assistant's full response to the 'messages' list
    st.session_state.messages.append({"role": "assistant", "content": response})

