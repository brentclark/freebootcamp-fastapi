# Use an official Python runtime as a parent image
FROM python:3
LABEL maintainer="Brent Clark <brentgclark@gmail.com>"

ARG UID=1000
ARG GID=1000
ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd --force --gid $GID app \
    && useradd --non-unique --home-dir /opt/app --create-home --uid $UID --gid $GID --comment "Application" app

# Set the working directory to /opt/app
WORKDIR /opt/app

# Clone the Git repository
RUN git clone https://github.com/brentclark/freebootcamp-fastapi.git .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite libraries
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Expose the port that Gunicorn will run on
EXPOSE 8000

USER app
# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
