FROM ubuntu:latest

RUN apt-get update && apt-get install -y git python3 python3-pip libpq-dev libcurl4-openssl-dev libssl-dev

RUN pip3 install pipenv tk

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY vriBackend /app/vriBackend

EXPOSE 8080

CMD ["flask", "--app", "vriBackend", "run", "--host", "0.0.0.0", "-p", "8080", "--debug"]