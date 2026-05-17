FROM rasa/rasa:3.6.1-full

USER root
COPY . /app
WORKDIR /app

RUN pip install --upgrade setuptools==65.5.0 wheel==0.38.4 cython==0.29.36

USER 1001
CMD ["run", "--enable-api", "--cors", "*", "--port", "7860", "--host", "0.0.0.0"]
