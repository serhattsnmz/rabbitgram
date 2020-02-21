FROM python:3.8-alpine

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python3.8 -m pip install -r requirements.txt

COPY ./rabbitgram/ ./rabbitgram/
COPY ./rabbitgram_console.py ./rabbitgram_console.py

ENTRYPOINT [ "python3.8", "./rabbitgram_console.py" ]