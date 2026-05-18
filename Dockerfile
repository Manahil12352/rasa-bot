FROM rasa/rasa:3.6.1-full

USER root

WORKDIR /app
COPY . /app

RUN rasa telemetry disable

USER 1001

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "7860", "--model", "models/20260519-004924-brown-sheave.tar.gz"]