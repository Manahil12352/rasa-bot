FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app
COPY . /app

RUN rasa telemetry disable

USER 1001

CMD ["run", "--enable-api", "--cors", "*", "-p", "10000"]