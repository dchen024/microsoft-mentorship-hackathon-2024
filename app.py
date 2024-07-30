from openai import OpenAI
import streamlit as st

st.title("FinFolio")
st.caption("Your AI financial advisor")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def get_avatar(role):
    return "person.png" if role == "user" else "finfolio.png"


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "person.png" if message["role"] == "user" else "finfolio.png"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="person.png"):
        st.markdown(prompt)

    # Prepare the context with the system message
    context = [{"role": "system", "content": "You are a helpful financial advisor to make personal finance easy. You are to only answer finance questions."}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant", avatar="finfolio.png"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=context,
            stream=True,
            temperature=0
        )
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})
