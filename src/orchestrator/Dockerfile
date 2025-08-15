FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade 'setuptools>=78.1.1' && \
    pip install -r requirements.txt && \
    python -m nltk.downloader punkt averaged_perceptron_tagger
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8081","--workers","2"]
