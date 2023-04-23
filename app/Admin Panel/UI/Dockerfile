FROM python:3.8-slim-buster

WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Set the environment variable for Streamlit
ENV STREAMLIT_SERVER_PORT=8080

# Expose the port on which the application will run
EXPOSE 8080

# Run the application
CMD ["streamlit", "run", "--server.port", "8080", "main.py"]
