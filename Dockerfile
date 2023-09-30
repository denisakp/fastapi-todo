FROM python:3.11-alpine

WORKDIR /todo

COPY ./requirements.txt /todo/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /todo/requirements.txt

COPY ./app /todo/app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]