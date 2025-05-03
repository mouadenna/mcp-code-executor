FROM python:3.10-slim

# Install Node.js and npm for JavaScript/TypeScript execution
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    g++ \
    default-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install TypeScript
RUN npm install -g typescript

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port for MCP server
EXPOSE 8000

# Run the server
CMD ["python", "code_executor_server.py"] 