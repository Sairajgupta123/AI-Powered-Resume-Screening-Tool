# AI‑Powered Resume Screener

A lightweight Streamlit web‑app that parses PDF/DOCX resumes, matches them against a job description with TF‑IDF + cosine similarity, and ranks candidates instantly.

## Quick Start (local)

```bash
# Clone and set up
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python setup_nltk.py
python -m spacy download en_core_web_sm

# Run
streamlit run app/main.py
```

Open <http://localhost:8501>, paste a JD, upload resumes, and download the ranked CSV.

## Deploy

* **Streamlit Community Cloud** — push this repo and link it. Nothing else needed.
* **Docker**
  ```Dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt && \
      python -m spacy download en_core_web_sm && \
      python setup_nltk.py && rm -rf ~/.cache/pip
  EXPOSE 8501
  CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
  ```

## Roadmap

- ✨ Swap TF‑IDF for Sentence Transformers embeddings.
- 🔒 Auto‑delete uploaded files after X hours.
- 📊 Add analytics page for HR dashboards.
