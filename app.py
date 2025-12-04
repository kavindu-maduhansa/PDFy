import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from htmlTemplates import css, bot_template, user_template

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
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # Return the vectorstore to be used for question answering
    return vectorstore

def handle_user_input(user_question, vectorstore):
    """Handle user questions and display chat history"""
    if vectorstore is None:
        st.warning("Please upload and process PDFs first!")
        return
    
    try:
        # Get relevant documents
        docs = vectorstore.similarity_search(user_question, k=3)
        
        if not docs:
            response = "I couldn't find any relevant information in your documents."
        else:
            # Create context from retrieved documents
            context_parts = []
            for i, doc in enumerate(docs, 1):
                context_parts.append(f"**Excerpt {i}:**\n{doc.page_content[:300]}...")
            
            response = "Based on your documents, here's what I found:\n\n" + "\n\n".join(context_parts)
        
        # Store in session state
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, I encountered an error while processing your question."})
    
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    
    # Apply custom CSS
    st.write(css, unsafe_allow_html=True)

    st.header("Chat with multiple PDFs :books:")
    
    # Initialize session state for chat history and vectorstore
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    
    # User input
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question, st.session_state.vectorstore)
    
    # Display chat history with custom templates
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your documents") 
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", 
            accept_multiple_files=True,
            type=['pdf'])
        
        if st.button("Process", type="primary"):
            if not pdf_docs:
                st.error("Please upload at least one PDF file!")
            else:
                with st.spinner("Processing your documents..."):
                    try:
                        # get pdf text
                        raw_text = get_pdf_text(pdf_docs)
                        
                        if not raw_text.strip():
                            st.error("No text could be extracted from the PDFs. Please make sure they contain readable text.")
                            return
                        
                        st.info(f"Extracted {len(raw_text)} characters from your PDFs")

                        # get text chunks
                        text_chunks = get_text_chunks(raw_text)
                        st.info(f"Split into {len(text_chunks)} chunks")

                        # create vector store
                        vectorstore = get_vectorstore(text_chunks)
                        
                        # Store vectorstore in session state
                        st.session_state.vectorstore = vectorstore
                        
                        # Clear previous chat history when new documents are processed
                        st.session_state.chat_history = []
                        
                        st.success(f"✅ Successfully processed {len(pdf_docs)} PDF(s)! You can now ask questions.")
                    
                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")
        
        # Add a clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
        
        # Display info
        if st.session_state.vectorstore is not None:
            st.info("📚 Documents loaded and ready!")
        else:
            st.warning("⚠️ No documents loaded yet")
        
if __name__ == '__main__':
    main()