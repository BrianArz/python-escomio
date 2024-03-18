# Use a lightweight version of Python for the initial build stage
FROM python:alpine3.19 as build

# Update the package list and install build dependencies
RUN apk update
RUN apk add --no-cache \
      build-base gcc

# Set the working directory for the build stage
WORKDIR /usr/app

# Create a Python virtual environment and activate it for subsequent commands
RUN python -m venv venv
ENV PATH="/usr/app/venv/bin:$PATH"

# Copy the Python dependencies file and install dependencies in the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Start a new stage from a lightweight Python base image
FROM python:alpine3.19

# Set the working directory for the application
WORKDIR /usr/app

# Copy the virtual environment from the build stage
COPY --from=build /usr/app/venv ./venv

# Copy the rest of the application code
COPY . .

# Ensure commands run inside the virtual environment
ENV PATH="/usr/app/venv/bin:$PATH"

# The command to run the application using Gunicorn as the web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
