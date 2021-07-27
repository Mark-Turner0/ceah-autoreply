FROM python:latest

WORKDIR /ceah-backend

COPY ./ .

CMD python3 -u main.py $MAILPASSWORD
