# Use official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code into the container
COPY . /app/

# Expose the port the app will run on (adjust if needed)
EXPOSE 5000

# Set the command to run your Flask application
CMD ["python", "app.py"]
