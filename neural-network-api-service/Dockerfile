# Set base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install ngrok -y

# Set NGROK authtoken (Replace YOUR_AUTHTOKEN with your actual token)
RUN ngrok config add-authtoken 2ocqCtL9ZhqtSqzm345OlafoVJh_6Ga7caePkvjUWLHcgPWd5

# Copy application files
COPY . .

# Expose port (modify if needed)
EXPOSE 8000

# Run the application
CMD ["python", "api/main.py"]
