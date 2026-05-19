FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app

# Copy everything from your repo into the container
COPY . /app

# --- Debug & Model Fix ---
# 1. Show what's in the models folder to help us debug
RUN echo "Contents of /app/models:" && ls -la /app/models/ || echo "No models folder found"
# 2. If a model exists, copy it to the default location Rasa expects
RUN mkdir -p /app/models && \
    MODEL_FILE=$(find /app -name "*.tar.gz" | head -n 1) && \
    if [ -n "$MODEL_FILE" ]; then \
        cp "$MODEL_FILE" /app/models/latest.tar.gz && \
        echo "Copied model from $MODEL_FILE to /app/models/latest.tar.gz"; \
    else \
        echo "ERROR: No model .tar.gz file found to copy!"; \
    fi

RUN rasa telemetry disable

# Switch to the non-root 'rasa' user
USER 1001

# The explicit and final CMD. It will only be used if the Render override is truly empty.
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "10000"]
