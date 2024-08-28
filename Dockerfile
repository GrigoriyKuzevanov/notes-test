FROM python:3.10

WORKDIR /usr/src/notes

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.11.0/wait /wait

RUN chmod +x /wait

CMD /wait && bash entrypoint.sh
