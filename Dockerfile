FROM python:latest

WORKDIR /ceah-autoreply

COPY ./ .

CMD python3 -u main.py $MAILPASSWORD
