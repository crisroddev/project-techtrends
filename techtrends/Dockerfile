FROM python:3.8

COPY . /app

WORKDIR /app

RUN pip3 --upgrade pip

EXPOSE 3111

CMD python init_db.py ; python app.py
