FROM alpine:3.6

RUN apk upgrade --update-cache

# Install permanent runtime dependencies
RUN apk add \
	python3 \
	mariadb-client-libs

# Install build dependencies required to install the PyPI packages below
RUN apk add --virtual build-deps \
	mariadb-dev \
	libc-dev \
	python3-dev \
	gcc

# Install permanent runtime dependencies from PyPI
RUN pip3 install \
	mysqlclient \
	pathvalidate \
	regex \
	ftfy \
	ujson

# Cleanup
RUN apk del build-deps \
&& rm -v /var/cache/apk/*

COPY redsym.py /srv/redsym/

COPY REDsym/ /srv/redsym/REDsym/

ENTRYPOINT python3 /srv/redsym/redsym.py update
