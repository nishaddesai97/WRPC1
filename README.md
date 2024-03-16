STEP 1 : Clone the Repository from GitHub.(https://github.com/PradipKanzariya/WRPC)

    git clone https://github.com/PradipKanzariya/WRPC.git

1.1 Change current working path.
    
    cd WRPC

1.2 : Create Static Directory

    mkdir static

STEP 2 : Create Virtual Environment

    virtualenv .venv

2.1 : Activate .venv
    
    .\.venv\Scripts\activate

2.2 : Install requirements.txt file
    
    pip install -r .\requirements.txt

STEP 3 : Run the python files on browser

    command - streamlit run <file name>
example - streamlit run .\WRPC_DSM_UI_Accounts.py
