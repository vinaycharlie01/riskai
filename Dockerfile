# Use official Python runtime
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port your API will run on (change if needed)
EXPOSE 8000

# Run the Python app with "api" argument
CMD ["python", "main.py", "api"]
