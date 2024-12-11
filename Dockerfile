# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /forex_api

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8081

# Command to run the FastAPI app using Uvicorn (ASGI server)
CMD ["uvicorn", "forex_api.main:app", "--host", "0.0.0.0", "--port", "8081"]
