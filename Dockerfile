FROM rasa/rasa:3.6.1-full

USER root
COPY . /app
RUN pip install --no-cache-dir google-generativeai

USER 1001
CMD ["run", "--enable-api", "--cors", "*", "--port", "7860", "--host", "0.0.0.0"]
