FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade 'setuptools>=78.1.1' && \
    pip install -r requirements.txt
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080","--workers","4"]
