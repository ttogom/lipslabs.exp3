
# Quiz

Download source code

    git clone https://github.com/evadelzz1/experiment3.git

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
