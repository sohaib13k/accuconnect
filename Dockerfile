FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /accuconnect

COPY . /accuconnect/

RUN mkdir -p /log

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "accuconnect.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]