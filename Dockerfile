FROM dullage/gunicorn:20.0-python3.8-alpine3.12

# Switch to root to install dependendies
USER root

# Install gcc Dependency
RUN apk add --update-cache \
    build-base \
 && rm -rf /var/cache/apk/*

# Switch back to the gunicorn user
USER gunicorn

COPY --chown=gunicorn ./app ./Pipfile ./Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
