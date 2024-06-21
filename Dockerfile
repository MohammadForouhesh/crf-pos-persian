FROM python:3.7.13-bullseye as builder

WORKDIR /usr/app

COPY /requirements.txt /usr/app/
COPY setup.* /usr/app/
COPY *.toml /usr/app/

RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py install

COPY . /usr/app/

CMD ["sh", "startup.sh"]
