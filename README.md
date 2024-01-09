
# Quiz
This program is to get an experiment with openai and streamlit in python.\
The program takes multiple pdf files and generates 5 multiple-choice questions for user to solve as well as showing the result of quiz.\
It should effectively serve as a reinforcement learning tool especially right before the exams.

To navigate to the customized implementation, direct yourself to `dev-sumin`.
> `main` contains the reference code

## How to execute
Download source code

    git clone https://github.com/ttogom/lipslabs.exp3.git

Setup virtual environment and setup python env variables

    cd ./experiment3

    pyenv versions

    pyenv local 3.11.6

    pyenv versions

    echo '.env'  >> .gitignore
    echo '.venv' >> .gitignore

    echo 'OPENAI_API_KEY=sk-9jz....' >> .env

    ls -la

    python -m venv .venv

    source .venv/bin/activate

    python -V

Download the libraries from requirements.txt

    pip install -r requirements.txt

Execute the program

    python -m streamlit run app.py

Deactivate venv

    deactivate
