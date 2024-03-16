STEP 1 : Clone the Repository from GitHub.(https://github.com/PradipKanzariya/WRPC)

    command - git clone https://github.com/PradipKanzariya/WRPC.git
    
    command - cd WRPC

    STEP 1.1 : Create Static Directory

    command - mkdir static

STEP 2 : Create Virtual Environment

    command - virtualenv .venv
    
    command - .\.venv\Scripts\activate
    
    command - pip install -r .\requirements.txt

STEP 3 : Run the python files on browser

    command - streamlit run <file name>
    example - streamlit run .\WRPC_DSM_UI_Accounts.py
