# Company Knowledge Base RAG Demo

This is a small interview-ready RAG-style demo. It loads local company knowledge files, splits them into chunks, retrieves the most relevant chunks for a user question, and generates an answer grounded in the retrieved context.

The first version uses only Python standard library code, so it can run without external packages or an API key.

## Run

```powershell
python rag_demo.py
```

Then ask questions such as:

- What kind of interns is the company looking for?
- What will interns work on?
- What skills are useful for this role?
- Is the internship onsite or remote?
- What is RAG?

Type `exit` to quit.

## How It Works

```text
Knowledge files
      ↓
Load text
      ↓
Chunk text
      ↓
Convert chunks and question into word-frequency vectors
      ↓
Cosine similarity search
      ↓
Top relevant chunks
      ↓
Grounded answer with sources
```

## Interview Talking Points

- RAG means Retrieval-Augmented Generation.
- Instead of asking the LLM to answer only from its memory, the system first retrieves relevant information from a private knowledge base.
- This reduces hallucination and lets the assistant answer using company-specific documents.
- In a production version, this simple vector search can be replaced with embeddings and a vector database such as FAISS, Chroma, Pinecone, or pgvector.
- The answer layer can be connected to an LLM API such as OpenAI, Gemini, Claude, or a local model.

## Possible Production Improvements

- Add PDF, DOCX, website, and database ingestion.
- Use embedding models instead of word-frequency vectors.
- Store vectors in Chroma, FAISS, Pinecone, or PostgreSQL with pgvector.
- Add a Streamlit, FastAPI, or React interface.
- Add source citations, user login, document permissions, Docker deployment, and logging.
