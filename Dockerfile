FROM python:3.13-slim
RUN mkdir /app
WORKDIR /app

# Install system dependencies for mysql-connector
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]