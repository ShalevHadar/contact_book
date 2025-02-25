FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app

# Install PostgreSQL client tools (for pg_isready)
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["bash", "entrypoint.sh"]

# Expose FastAPI default port
EXPOSE 8000

# Correct CMD for FastAPI with Uvicorn
CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
