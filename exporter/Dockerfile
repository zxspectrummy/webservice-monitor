FROM python:3.10

RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -yq nodejs

RUN npm i -g nodemon

COPY requirements.txt /usr/src/app/requirements.txt
COPY exporter.py /usr/src/app/

WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
CMD nodemon --exec python3 exporter.py