FROM python:3.9

RUN mkdir /opt/bot
WORKDIR /opt/bot

COPY *.py requirements.txt ./

RUN pip3 install -r requirements.txt

CMD ["python3", "/opt/bot/main.py"]