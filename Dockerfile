FROM python:3.13.1

WORKDIR /server

COPY rexec_server /server/rexec_server
COPY requirements.txt /server
COPY run_server.py /server

RUN pip install -r requirements.txt

ENV broker_addr=127.0.0.1
ENV broker_port=5560

CMD ["sh", "-c", "python run_server.py ${broker_addr} \
                                        --broker_port ${broker_port}"]