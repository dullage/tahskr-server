FROM dullage/gunicorn:20.0-python3.8-alpine3.12

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app
