# PDFy - Chat with Multiple PDFs 📚

A Streamlit-based application that allows you to upload multiple PDF documents and ask questions about their content using AI-powered semantic search.

## Features

✨ **Multi-PDF Support** - Upload and process multiple PDF files simultaneously
🔍 **Semantic Search** - Find relevant information across all your documents
💬 **Chat Interface** - Interactive chat with beautiful UI and avatars
📝 **Context-Aware** - Get answers with relevant excerpts from your documents
🎨 **Custom Styling** - Professional chat interface with custom CSS
💾 **Session Memory** - Chat history persists during your session

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kavindu-maduhansa/PDFy.git
   cd PDFy
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file (optional - for OpenAI):**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Run the application:**
   ```bash
   .\venv\Scripts\streamlit.exe run app.py
   ```

2. **Upload PDFs:**
   - Click on "Browse files" in the sidebar
   - Select one or more PDF files
   - Click the "Process" button

3. **Ask Questions:**
   - Type your question in the text input
   - Press Enter to get answers from your documents
   - View the chat history with relevant excerpts

## Project Structure

```
PDFy/
├── app.py                  # Main Streamlit application
├── htmlTemplates.py        # CSS and HTML templates for chat UI
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── venv/                  # Virtual environment (not in git)
└── README.md              # This file
```

## Technologies Used

- **Streamlit** - Web application framework
- **PyPDF2** - PDF text extraction
- **LangChain** - LLM application framework
- **FAISS** - Vector database for semantic search
- **HuggingFace Embeddings** - Text embeddings (works offline)
- **Sentence Transformers** - State-of-the-art sentence embeddings

## Features in Detail

### PDF Processing
- Extracts text from multiple PDFs
- Splits text into manageable chunks
- Creates vector embeddings for semantic search

### Chat Interface
- Beautiful custom-styled chat bubbles
- User and bot avatars
- Scrollable chat history
- Real-time responses

### Semantic Search
- Uses HuggingFace's instructor-xl model
- Finds the 3 most relevant excerpts
- No API keys required for basic functionality

## Configuration

### Using OpenAI Embeddings (Optional)
To use OpenAI embeddings instead of HuggingFace:

1. Add your OpenAI API key to `.env`
2. In `app.py`, uncomment line 29:
   ```python
   embeddings = OpenAIEmbeddings()
   ```
3. Comment out line 30:
   ```python
   # embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
   ```

## Troubleshooting

### Import Errors
If you see import errors, make sure:
1. Virtual environment is activated
2. All packages are installed: `pip install -r requirements.txt`
3. VS Code is using the correct Python interpreter from `venv`

### Streamlit Not Found
Run Streamlit using the full path:
```bash
.\venv\Scripts\streamlit.exe run app.py
```

### PDF Processing Errors
- Ensure PDFs contain readable text (not scanned images)
- Try with smaller PDFs first
- Check that files are valid PDF format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**Kavindu Maduhansa**
- GitHub: [@kavindu-maduhansa](https://github.com/kavindu-maduhansa)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://python.langchain.com/)
- Embeddings by [HuggingFace](https://huggingface.co/)
