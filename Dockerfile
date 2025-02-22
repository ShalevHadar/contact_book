# Use a lightweight Python base image
FROM python:3.10-slim

# Set a working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Debug: Show what files are in the build context *before* we copy "server"
# This will list everything Docker "sees" at this point, which is your entire build context.
RUN echo "===== BUILD CONTEXT (before copying 'server') =====" && ls -Ral .

# Copy the entire `server` directory into /app/server
COPY . /app/server

# Debug: Now that we copied, let's see what's in /app/server
RUN echo "===== /app directory after copying 'server' =====" && ls -Ral /app

# Expose the port FastAPI will run on (e.g. 8000)
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
