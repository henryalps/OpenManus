FROM python:3.9

RUN apt-get update && apt-get -y install tree

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "/app/docker/unified/start.sh"]