FROM python:3.11

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt


ADD . .
RUN chmod +x ./startup.sh

EXPOSE 3000
CMD ["/bin/bash","-c","./startup.sh"] 