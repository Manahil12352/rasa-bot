FROM rasa/rasa:3.6.1-full

USER root
COPY . /app
WORKDIR /app

USER 1001
CMD ["run", "--enable-api", "--cors", "*", "-p", "7860", "-i", "0.0.0.0"]
