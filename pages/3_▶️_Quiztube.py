import streamlit as st

from helpers.youtube_utils import extract_video_id_from_url
from helpers.youtube_utils import get_transcript_text
from helpers.openai_utils import get_quiz_data
from helpers.quiz_utils import string_to_list, get_randomized_options

st.set_page_config(
    page_title="QuizTube",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("QuizTube", anchor=False)
st.write("""

1. Paste the YouTube video URL.
2. Enter your [OpenAI API Key](https://platform.openai.com/account/api-keys).

⚠️ Important: The video **must** have English captions for the tool to work.


""")

with st.form("user_input"):
    YOUTUBE_URL = st.text_input("Enter the YouTube video link:",
                                placeholder="https://youtube.com/")
    OPENAI_API_KEY = st.text_input(
        "Enter your OpenAI API Key:", placeholder="sk-XXXX", type='password').encode('ascii', 'ignore').decode('ascii')
    submitted = st.form_submit_button("Craft my quiz!")

if submitted or ('quiz_data_list' in st.session_state):
    if not YOUTUBE_URL:
        st.info(
            "Please provide a valid YouTube video link. Head over to [YouTube](https://www.youtube.com/) to fetch one.")
        st.stop()
    elif not OPENAI_API_KEY:
        st.info(
            "Please fill out the OpenAI API Key to proceed. If you don't have one, you can obtain it [here](https://platform.openai.com/account/api-keys).")
        st.stop()

    with st.spinner("Crafting your quiz..."):
        if submitted:
            video_id = extract_video_id_from_url(YOUTUBE_URL)
            video_transcription = get_transcript_text(video_id)
            quiz_data_str = get_quiz_data(video_transcription, OPENAI_API_KEY)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [
                    None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Your Quiz:", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[
                    i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                # Update the stored answer right after fetching it
                st.session_state.user_answers[i] = user_choice_index

            results_submitted = st.form_submit_button(label='How did I do?')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(
                    zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f'''Your score:
                           {score}/{len(st.session_state.quiz_data_list)}''')

                # Check if all answers are correct
                if score == len(st.session_state.quiz_data_list):
                    st.balloons()
                else:
                    incorrect_count = len(
                        st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(
                            f"Almost perfect! You got 1 question wrong. Let's review it:")
                    else:
                        st.warning(f'''Almost there! You got
                                   {
                                   incorrect_count} questions wrong. Let's review them:''')

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")