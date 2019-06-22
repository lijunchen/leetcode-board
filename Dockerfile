FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libxml2-dev libxslt-dev python-dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80
COPY . .
CMD ["python3", "run_in_docker.py"]
