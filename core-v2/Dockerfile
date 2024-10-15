FROM public.ecr.aws/docker/library/python:3.11.6 AS builder

WORKDIR /usr/app
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM public.ecr.aws/docker/library/python:3.11.6 AS production

COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

ADD . .
RUN chmod +x ./startup.sh

EXPOSE 3000
CMD ["/bin/bash","-c","./startup.sh"]