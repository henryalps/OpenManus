FROM python:3.9

RUN apt-get update && apt-get -y install tree dos2unix

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Fix line endings for shell scripts
RUN dos2unix /app/docker/unified/start.sh && \
    chmod +x /app/docker/unified/start.sh

CMD ["/bin/bash", "/app/docker/unified/start.sh"]