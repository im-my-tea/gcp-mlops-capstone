FROM python:3.9-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

#we bind to 0.0.0.0 (External access) and Port 80 (Standard Web Port)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]