FROM debian:stretch

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY script.py .

CMD [ "python3", "./script.py" ]
