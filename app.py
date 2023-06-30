import streamlit as st
from PyPDF2 import PdfReader
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS  # for storing embeddings in a vector store locally. 
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory, ConversationKGMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain.llm import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from htmlTemplates import css, bot_template, user_template

load_dotenv()

def get_pdf_text(pdf_docs):
    text = ""

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vectorStore):
    # llm = ChatOpenAI(model_name='gpt-4')
    llm = ChatOpenAI()
    # memory = ConversationKGMemory(memory_key='chat_history', llm=llm, return_messages=True)  # we are using graph memory to store the conversation.
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorStore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userInput(user_question):
    if st.session_state.conversation is not None:
        chat_history = [] if st.session_state.chat_history is None else st.session_state.chat_history
        response = st.session_state.conversation({'question' : user_question, 'chat_history': chat_history})
        st.session_state.chat_history = response['chat_history']
        
        # st.write(response)
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.write("Please upload a PDF document and click 'Process' before asking any question.")

def main():
    st.set_page_config(page_title="Chat with PDF", page_icon=":books:")

    st.write(css, unsafe_allow_html=True) # css is always added on top
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with your PDFs")
    user_question = st.text_input("Ask a question about your documents", placeholder="Ask me any question about your documents", help="Ask me any question about your documents")
    if user_question:
        handle_userInput(user_question)

    # st.write(user_template.replace("{{MSG}}", "Hello I am Uncle Roger"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "Hello I am Mia"), unsafe_allow_html=True)


    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs and click on 'Process'", type="pdf", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing your documents..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # it will take list of pdfs and return a single big list of string. 
                
                # get text chunks
                text_chunks = get_text_chunks(raw_text)

                # create our vector store.
                vectorStore = get_vector_store(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorStore)
                # st.session_state means that the variable will be stored in the session and it will not be reintialized when the page is refreshed.
                # the other benefit of this is that we can use this variable in other functions as well or globally anywhere in the code/app.
    
if __name__ == "__main__":
    main()
