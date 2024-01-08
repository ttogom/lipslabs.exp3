import streamlit as st
from utils.pdf_utils import pdf_to_text

# config
st.set_page_config(
    page_title="QuizYourPDF",
    page_icon="",
    layout="centered"
)

# body
st.title(":blueQuizPDF — Learn Your Lectures 🧠", anchor=False)
st.write("""
Ever had a trouble studying for an exam a night before? Use QuizPDF to go over your lecture concepts quickly in an efficient manner!

**How does it work?** 🤔
1. Drop PDF of your lectures from the class
2. Enter your [OpenAI API Key](https://platform.openai.com/account/api-keys).

Once you've input the details, voilà! Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the PDF. Let's put your knowledge to the test!""")
st.divider()

# input
uploaded_files = st.file_uploader('Upload your PDFs here and click \'Start\'', type="pdf", accept_multiple_files=True)
started = st.button("Start")
if started or ('quiz_data' in st.session_state):
    with st.spinner("Creating your quiz..."):
        raw_txt = pdf_to_text(uploaded_files)