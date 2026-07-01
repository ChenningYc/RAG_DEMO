# Company Knowledge Base RAG Demo

This is an interview-ready RAG-style AI assistant demo. It loads local company knowledge files, splits them into chunks, retrieves relevant chunks based on a user question, and displays grounded answers with source files.

The project is intentionally lightweight. It uses only the Python standard library, so it can run without external packages, paid APIs, or an internet connection.

## Project Goal

The goal is to demonstrate the core workflow behind a company knowledge-base AI assistant:

- Load internal knowledge documents.
- Split long documents into smaller chunks.
- Convert questions and chunks into simple word-frequency vectors.
- Compare the question with each chunk using cosine similarity.
- Return the most relevant information with source references.
- Provide both command-line and web-based interaction.

## Features

- Local knowledge base stored in `knowledge_base/`.
- Simple RAG-style retrieval pipeline.
- Word-frequency vectorization using Python `Counter`.
- Cosine similarity ranking.
- Source file display for retrieved chunks.
- Command-line demo with `rag_demo.py`.
- Simple web frontend with `web_app.py` and files in `static/`.
- Dockerfile for containerized deployment.

## Run Command-Line Demo

```powershell
python rag_demo.py
```

Example questions:

- What kind of interns is the company looking for?
- What will interns work on?
- What skills are useful for this role?
- Is the internship onsite or remote?
- What is RAG?
- What is an AI agent?
- What is prompt engineering?
- What is Docker used for?
- What are embeddings and vector databases?
- Tell me about Yu Chengyan.
- Why are you interested in this internship?

Type `exit` to quit.

## Run Web Demo

```powershell
python web_app.py
```

Then open:

```text
http://127.0.0.1:8000
```

The web version lets users type questions in a browser. The frontend sends the question to a local Python API, and the backend returns the retrieved answer with source files and similarity scores.

## Run with Docker

Build the Docker image:

```powershell
docker build -t rag-demo .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 rag-demo
```

Then open:

```text
http://127.0.0.1:8000
```

## Architecture

```text
Knowledge files
      |
      v
Load text files
      |
      v
Split text into chunks
      |
      v
Create word-frequency vectors
      |
      v
Receive user question
      |
      v
Vectorize the question
      |
      v
Calculate cosine similarity
      |
      v
Retrieve top matching chunks
      |
      v
Display answer and sources
```

## Key Files

- `rag_demo.py`: Core RAG-style retrieval logic and command-line interface.
- `web_app.py`: Local HTTP server and `/api/ask` endpoint.
- `static/index.html`: Web page structure.
- `static/styles.css`: Web UI styling.
- `static/app.js`: Frontend request and rendering logic.
- `knowledge_base/`: Local text files used as the knowledge base.
- `Dockerfile`: Container setup for running the web app.

## Knowledge Base Files

- `company_role.txt`: Company role description and internship overview.
- `work_scope.txt`: Tasks interns may work on.
- `candidate_profile.txt`: Candidate requirements.
- `internship_details.txt`: Internship benefits and company details.
- `rag_basics.txt`: RAG concept explanation.
- `ai_agents.txt`: AI agent concepts and business use cases.
- `prompt_engineering.txt`: Prompt structure and RAG prompt rules.
- `docker_basics.txt`: Docker concepts for deployment.
- `embedding_vector_db.txt`: Embeddings and vector database basics.
- `interview_profile.txt`: Candidate profile and internship motivation.
- `interview_qa.txt`: Common English interview questions and sample answers.

## Current Limitations

- The demo uses word-frequency vectors, not real embeddings.
- It searches by keyword overlap more than semantic meaning.
- It supports local `.txt` files only.
- It does not connect to an external LLM API yet.
- It does not include user login, file upload, logging, or production monitoring.

## Future Improvements

- Replace word-frequency search with embeddings.
- Store vectors in Chroma, FAISS, Pinecone, or PostgreSQL with pgvector.
- Connect an LLM API such as OpenAI, Gemini, Claude, or a local model.
- Add PDF, DOCX, website, and database ingestion.
- Add file upload and automatic re-indexing.
- Add authentication, logging, evaluation, and monitoring.
- Deploy with Docker to a cloud server.

## Interview Talking Points

- RAG means Retrieval-Augmented Generation.
- The system searches relevant knowledge first, then answers based on that knowledge.
- Chunking helps split long documents into smaller searchable pieces.
- Cosine similarity helps rank which chunks are most related to the user question.
- This project is an MVP that demonstrates the RAG workflow clearly.
- In production, the simple vector search should be replaced with embeddings and a vector database.
- Docker makes the application easier to run consistently across different environments.

## Short Demo Explanation

```text
This is a lightweight company knowledge-base RAG demo.

It loads local documents, splits them into chunks, converts the chunks and user question into word-frequency vectors, calculates cosine similarity, and returns the most relevant chunks with sources.

I also added a simple web frontend and a Dockerfile so the project is closer to a real deployable application.

The current version is an MVP. In production, I would use embeddings, a vector database, an LLM API, file upload, authentication, logging, and Docker-based deployment.
```
