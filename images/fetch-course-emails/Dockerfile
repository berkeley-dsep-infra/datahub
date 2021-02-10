FROM ubuntu:20.04

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		git \
		python3 \
		python3-dev \
		python3-pip \
		python3-setuptools \
		python3-wheel \
		jq \
		vim-tiny

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

ADD course-emails.py /usr/local/bin/

CMD ["/usr/local/bin/course-emails.py", "-v"]
