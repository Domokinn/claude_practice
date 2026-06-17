import streamlit as st
import anthropic

st.title("ECU技術アシスタント")
st.caption("車載システムに関する質問に答えます")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("質問を入力してください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = anthropic.Anthropic()
    
    with st.chat_message("assistant"):
        response_text = ""
        placeholder = st.empty()
        
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=1024,
            system="あなたは車載システムの技術専門家です。ECUやCAN通信、機能安全について詳しく答えてください。",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        ) as stream:
            for text in stream.text_stream:
                response_text += text
                placeholder.markdown(response_text)
        
    st.session_state.messages.append({"role": "assistant", "content": response_text})