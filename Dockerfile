FROM jenkins/jenkins:lts-jdk21

USER root

# Installing necessary dependencies (python, pip, clang, and build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installing security tools for Jenkins
RUN python3 -m pip install --no-cache-dir --break-system-packages \
    bandit semgrep detect-secrets pip-audit

# Preparing the application workspace
WORKDIR /app

# Copying rest of the code
COPY . /app

USER jenkins