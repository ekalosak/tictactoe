FROM python:3.7.4-buster

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "/bin/bash" ]
