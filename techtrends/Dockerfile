FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip --upgrade pip

EXPOSE 3111

CMD python init_db.py ; python app.py
