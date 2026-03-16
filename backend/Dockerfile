FROM python:3.11-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application
COPY . .

# expose port
EXPOSE 8000

# train model (if needed) and start server
CMD ["sh", "-c", "python -m app.models.train_yield_model && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
