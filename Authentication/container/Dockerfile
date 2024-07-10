FROM python:3.12.2-alpine3.19

WORKDIR /app

RUN addgroup -g 1000 app && adduser -D -u 1000 -G app app
COPY --chown=app ../ .

RUN apk update && apk add --no-cache curl
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install flask
RUN pip install pymongo
RUN pip install flask_swagger_ui
RUN pip install marshmallow

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://127.0.0.1:8000/healthcheck || exit 1

USER app 

ENV MONGODB_USER=admin
ENV MONGODB_PASS=secret
ENV MONGODB_HOST=mongo_db

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "-w 4", "app:app"]
