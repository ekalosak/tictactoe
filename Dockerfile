FROM python:3.7.4-buster

COPY game.py requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "game.py" ]
