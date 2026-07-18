FROM jenkins/jenkins:lts-jdk21

USER root

# Installing necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Preparing the application workspace
WORKDIR /app

# Copying rest of the code
COPY . /app

USER jenkins