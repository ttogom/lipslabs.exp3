import streamlit as st
# from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
import time
import base64
import tempfile
def initialize():
    if 'q' not in st.session_state:
        st.session_state.q = []

def display_pdf(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
def quizzer(pdf_text, OPENAI_API_KEY):
    api_key = OPENAI_API_KEY.encode('ascii', 'ignore').decode('ascii')
    llm = OpenAI(openai_api_key=api_key)
    
    prompt_template = PromptTemplate.from_template(
        '''Provide a multiple-choice question with only ONE correct answer and the answer from this text: 
        {pdf_file}
        
        Follow this template:
            Question: (Question)
            A. (multiple choice)
            B. (multiple choice)
            C. (multiple choice)
            D. (multiple choice)
            (Correct Answer)
        
        Example: 
            Question: What run should you take to warm up on Blackcomb Mountain?
            A. Easy Out
            B. Countdown
            C. Big Easy
            D. Magic Castle
            C. Big Easy
        '''
    )
    quiz = prompt_template.format(pdf_file=pdf_text)
    
    return llm(quiz)

def quizzing(i, noq, pdf_text, time_limit, OPENAI_API_KEY):
    global corrects
    
    st.session_state.q.append(quizzer(pdf_text, OPENAI_API_KEY))
    question = st.session_state.q[i].split('?')
    
    st.subheader('Question ' + str(i + 1))
        
    st.write(question[0][10:] + '?')
    
    mc = question[1].split('.')
    
    mc_choice = st.radio(
        "multiple choice",
        label_visibility="collapsed",
        options=(mc[1][:-1], mc[2][:-1], mc[3][:-1], mc[4][:-1]),
        index=None, 
    )
    
    correct_ans = mc[5]

    if mc_choice is not None:
        if str(correct_ans).strip() == str(mc_choice).strip():
            st.info(f"Correct 🟢 You selected '{mc_choice}'")
            corrects += 1
        else: 
            st.info(f"You selected '{mc_choice}'")
            st.error(f"Incorrect 🔴 Correct answer is '{correct_ans}'. ")
    
    if mc_choice is None:
        st.error(f"Out of time! 🔴 Correct answer is '{correct_ans}'. ")

def main():
    initialize()
    
    # if not load_dotenv():
    #     st.info("Could not load .env file or it is empty. Please check if it exists and is readable.")
    #     exit(1)
    
    # st.set_page_config(
    #     page_title="Quizzer❔",
    #     page_icon="❔" 
    # )
    
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("Go to", ["Home", "PDF Viewer", "Quiz"])
    
    if selected_page == "Home":
        st.header("Welcome to Quizzer❔")
        st.write("Use the sidebar to navigate between pages.")

    elif selected_page == "PDF Viewer":
        st.header("PDF Viewer 📄")
        pdf = st.file_uploader("Upload your PDF", type="pdf")
        if pdf is not None:
            st.subheader("PDF Content")

            # Save the PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf.read())

            # Display the PDF from the temporary file
            display_pdf(temp_file.name)

            # Remove the temporary file
            os.remove(temp_file.name)


    elif selected_page == "Quiz":
        st.header('Quizzer❔')
    
    
        col1, col2 = st.columns(2)
    
        with col1:
            noq = st.selectbox(
                "Number of questions for your quiz:",
                key='number_of_questions',
                options=[5, 10, 15, 20, 25, 30]
            )
        with col2:
            time_limit = st.selectbox(
                "Time limit (in seconds) for each question",
                key='time_limit',
                options=[15, 30, 45, 60, 75, 90, 105, 120]
            )
    
        pdf = st.file_uploader("Upload your PDF", type="pdf")
        cancel_button = st.button('Cancel')
    
        if cancel_button:
            st.stop()
        
        global corrects
        corrects = 0

        with st.form("user_input"):
            OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password').encode('ascii', 'ignore').decode('ascii')
            started = st.form_submit_button("Start")

        if pdf is not None and started:
            st.empty()
            pdf_reader = PdfReader(pdf)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
        
            j = 0

            while j < noq:
                quizzing(j, noq, pdf_text, time_limit, OPENAI_API_KEY)
                j += 1
                
            st.subheader(f"Quiz Finished! Your score is {str(corrects)} / {noq}. ")

if __name__ == '__main__':
    main()