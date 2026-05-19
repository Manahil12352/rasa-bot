FROM rasa/rasa:3.6.1-full

USER root
WORKDIR /app

# Copy everything from your project into the container
COPY . /app

# --- CRITICAL PART: Ensure the model is in the default location ---
# First, list the models to debug (this will show in build logs)
RUN echo "Contents of /app/models:" && ls -la /app/models/

# Create the default model directory and copy your trained model there
RUN mkdir -p /app/models
RUN cp /app/models/20260519-101800-international-resin.tar.gz /app/models/latest.tar.gz

# Disable telemetry
RUN rasa telemetry disable

# Switch back to the rasa user
USER 1001

# Run Rasa - it will automatically load the model from /app/models
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "10000"]
