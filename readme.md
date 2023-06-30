# Chat with your PDFs

Chat with PDFs is a Python application built with Streamlit and Langchain that allows users to upload PDF documents and interact with the content in a conversational manner. 

## Features

- Upload multiple PDF documents and process them into a conversational format.
- Ask questions and receive responses based on the content of your documents.
- The application uses the LangChain library for advanced conversational AI, which allows for dynamic, context-aware responses.
- Uses vector stores and embeddings for efficient content retrieval.

## Architecture
------------

![MultiPDF Chat App Diagram](./docs/PDF-LangChain.jpg)

The diagram and code is learnt from the tutorial [YouTube](https://youtu.be/dXxQ0LR-3Hg). 

I added some further checks and will be modifying code further according to my usecase in the coming days.
Feel free to reachout on my linkedin for any query. Linkedin link is given on my github main page profile.  


## Installation

1. Clone the repository:
\```bash
git clone https://github.com/furqan4545/chat_with_your_pdfs_AI.git
\```

2. Change directory to the downloaded folder:
\```bash
cd yourrepository
\```

3. Set up a virtual environment and activate it (optional but recommended):
\```bash
python3 -m venv env
source env/bin/activate
\```

4. Install the required dependencies:
\```bash
pip install -r requirements.txt
\```

## Usage

To start the app, simply run:
\```bash
streamlit run app.py
\```

This will start the Streamlit server and the app should be accessible at localhost:8501 in your browser.

In the sidebar, you can upload your PDFs. After uploading, click "Process" to process the documents. Once the documents are processed, you can ask questions about your documents in the text input box.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
