# Use the official Python base image
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy your index.html file to the container
COPY index.html .

# Expose port 80
EXPOSE 80

# Run the HTTP server when the container starts
CMD ["python", "-m", "http.server", "80"]