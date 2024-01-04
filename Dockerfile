# Use an official Python runtime as a parent image
FROM python:3
LABEL maintainer="Brent Clark <brentgclark@gmail.com>"

# Set the working directory to /app
WORKDIR /app

# Clone the Git repository
RUN git clone https://github.com/brentclark/freebootcamp-fastapi.git .

# Upgrade pip
RUN pip install --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Define environment variables
ENV APP_MODULE=your_app_module:app

# Command to run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--log-level", "info", "${APP_MODULE}"]
