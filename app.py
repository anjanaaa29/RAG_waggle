import streamlit as st
import sys
sys.path.append("src")

from src.rag import retrieve_chunks, generate_answer

st.set_page_config(page_title="MyWaggle FAQ Chatbot", page_icon="🤖")
st.title("🤖 MyWaggle FAQ Chatbot")

st.write("Ask questions about MyWaggle FAQs")

# Session state
if "answer" not in st.session_state:
    st.session_state.answer = ""

# Text input (Enter triggers rerun automatically)
question = st.text_input("Your question:")

# When user enters a question
if question.strip():
    with st.spinner("Fetching answer..."):
        chunks = retrieve_chunks(question)
        if not chunks:
            st.session_state.answer = "Sorry, no relevant FAQ found."
        else:
            st.session_state.answer = generate_answer(question, chunks)

# Display answer
if st.session_state.answer:
    st.subheader("Answer")
    st.success(st.session_state.answer)

    # Clear button BELOW answer
    if st.button("Clear"):
        st.session_state.question= ""
        st.session_state.answer = ""
        st.rerun()

