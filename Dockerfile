FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app

# Copy everything from your project into the container
COPY . /app

# Copy model to default location
RUN mkdir -p /app/models
RUN cp /app/models/*.tar.gz /app/models/latest.tar.gz 2>/dev/null || echo "No model found"

# Disable telemetry
RUN rasa telemetry disable

USER 1001

# Correct CMD - no duplicate "rasa"
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "10000"]
