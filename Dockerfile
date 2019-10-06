FROM python:3.7-alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN pip install -U pip

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi libffi-dev g++ postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir db
COPY main.py main.py
COPY db/__init__.py db/__init__.py
COPY process_chars_freq.py process_chars_freq.py
COPY parse_syllable_html.py parse_syllable_html.py
# CMD python main.py
ENTRYPOINT [ "python" ]

