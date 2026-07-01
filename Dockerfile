FROM python:3.11-slim

WORKDIR /app

COPY rag_demo.py web_app.py ./
COPY knowledge_base ./knowledge_base
COPY static ./static

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["python", "web_app.py"]


