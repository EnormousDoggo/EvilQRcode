# Use the official Python base image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy your index.html file to the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Run the HTTP server when the container starts
CMD ["python", "main.py"]
