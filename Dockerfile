FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app

# Copy everything including models
COPY . /app

# Verify models are there during build
RUN echo "=== Models found in /app/models ===" && \
    ls -la /app/models/ && \
    echo "=== Total size of models ===" && \
    du -sh /app/models/

# Disable telemetry
RUN rasa telemetry disable

# Switch to rasa user
USER 1001

# Simple command - no duplication
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "10000"]
