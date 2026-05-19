FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app

# Copy everything
COPY . /app

# Copy model to a specific location
RUN mkdir -p /app/models && \
    cp /app/models/20260519-101800-international-resin.tar.gz /app/models/model.tar.gz

RUN rasa telemetry disable

USER 1001

# Explicitly tell Rasa exactly which model file to use
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "10000", "--model", "/app/models/model.tar.gz"]
