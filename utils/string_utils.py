import random
import streamlit as st
import ast

def string_to_2d_list(quiz_data):
    try:
        print(quiz_data)
        return ast.literal_eval(quiz_data.get('text'))
        # return ast.literal_eval(quiz_data)
    except (SyntaxError, ValueError) as e:
        st.error(f"Error: The provided input is not correctly formatted. {e}")
        st.stop()

def get_randomized_options(options):
    correct_answer = options[0]
    random.shuffle(options)
    return options, correct_answer