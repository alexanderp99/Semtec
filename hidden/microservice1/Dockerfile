FROM python:3.12
WORKDIR /app
COPY old_rq_statements/requirements.txt .
COPY app.py .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]