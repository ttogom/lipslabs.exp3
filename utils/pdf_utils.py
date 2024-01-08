from PyPDF2 import PdfReader

def pdf_to_text(uploaded_files) -> str:
    """ This function takes multiple pdf files and return its raw text as a string.
    Argument(s) : List[]
    Return type : str
    """
    raw_txt = ""

    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            raw_txt += page.extract_text()

    return raw_txt