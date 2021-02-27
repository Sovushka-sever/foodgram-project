FROM python:3.8.5

WORKDIR /code
COPY . /code

RUN pip install --upgrade pip && \
    pip install -r /code/requirements.txt && \
    chmod +x /code/start.sh

CMD /code/start.sh
