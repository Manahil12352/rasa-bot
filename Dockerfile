FROM rasa/rasa:3.6.1-full

USER root
COPY . /app
WORKDIR /app

RUN chmod +x start.sh

USER 1001
CMD ["./start.sh"]
