import streamlit as st
from utils.pdf_utils import pdf_to_text
from utils.openai_utils import get_quiz_data
from utils.string_utils import *
from langchain_community.document_loaders import YoutubeLoader

# config
st.set_page_config(
    page_title="Quizzeria",
    page_icon="",
    layout="centered"
)

# body
st.title("🍕 Learn Your Lectures 🍕", anchor=False)
st.write("""
Ever had a trouble studying for an exam a night before? Use Quiznything to go over your lecture concepts quickly in an efficient manner!

1. Select the media type you would want to insert
1. Drop an appropriate file or text
2. Enter your [OpenAI API Key](https://platform.openai.com/account/api-keys).

Dive deep into questions crafted just for you, ensuring you've truly grasped the content of the subject. Let's put your knowledge to the test!""")
st.divider()


# options = st.selectbox(
#    "Choose file type you want?",
#    ("PDF", "Youtube Link", "Text"),
#    index=None,
#    placeholder="Select media type...",
# )

options = ("PDF", "Youtube Link", "Text")
index = st.selectbox("Choose file type you want", range(len(options)), format_func=lambda x: options[x], placeholder="Select media type...")


# input
# uploaded_files = st.file_uploader('Upload your PDFs here and click \'Start\'', type="pdf", accept_multiple_files=True)
if index == 0:
    uploaded_files = st.file_uploader('Upload your PDFs here and click \'Start\'', type="pdf", accept_multiple_files=True)
elif index == 1:
    uploaded_link = st.text_input("Enter Youtube Video ID here")
elif index == 2:
    uploaded_text = st.text_input("Enter some text 👇")


with st.form("user_input"):
    OPENAI_API_KEY = st.text_input("Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password')
    started = st.form_submit_button("Start")

# started = st.button("Start")
if started or ('quiz_data' in st.session_state):
    # if not uploaded_files:
    #     st.info("Please provide a .pdf file type.")
    #     st.stop()
    if index is None:
        st.info("Please provide a file type.")
        st.stop()
    if not OPENAI_API_KEY:
        st.info("Please provide a OpenAI API Key to proceed.")
        st.stop()

    OPENAI_API_KEY = OPENAI_API_KEY.encode('ascii', 'ignore').decode('ascii')

    # if index == 0:
    #     uploaded_files = st.file_uploader('Upload your PDFs here and click \'Start\'', type="pdf", accept_multiple_files=True)
    # elif index == 1:
    #     uploaded_link = st.text_input("Enter Youtube Video ID here")
    # elif index == 2:
    #     uploaded_text = st.text_input("Enter some text 👇")
    # else:
    #     st.info("Please provide a file type.")
    #     st.stop()

    with st.spinner("Creating your quiz..."):
        if started:
            
            if index == 0:
                raw_txt = pdf_to_text(uploaded_files)
                quiz_data = get_quiz_data(raw_txt, OPENAI_API_KEY)
            elif index == 1:
                loader = YoutubeLoader.from_youtube_url(uploaded_link, add_video_info=True)
                transcript = loader.load()
                quiz_data = get_quiz_data(transcript, OPENAI_API_KEY)
            elif index == 2:
                quiz_data = get_quiz_data(uploaded_text, OPENAI_API_KEY)
            st.session_state.quiz_data = string_to_2d_list(quiz_data)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Let's Test Your Knowledge..", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index  # Update the stored answer right after fetching it


            results_submitted = st.form_submit_button(label='Submit')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data)}")

                if score == len(st.session_state.quiz_data):  # Check if all answers are correct
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")
    