FROM python:3.7.4-slim-buster

ADD requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ADD . .

CMD ['python3', 'rebalancer.py']