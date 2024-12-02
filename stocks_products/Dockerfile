FROM python:3.9

COPY . .

RUN pip install -r requirements.txt

ENV DB_NAME=db.sqlite3

RUN python manage.py migrate

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
