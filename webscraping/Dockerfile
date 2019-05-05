FROM python:3

MAINTAINER Will Karnasiewicz <willkarnasiewicz@gmail.com>

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY OWGR-scrape.py /

CMD ["python", "./OWGR-scrape.py"]