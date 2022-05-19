# alpine is know as the most lightweight os, suitable for development
FROM python:3.10.4-alpine

# add packages for psycopg2
RUN apk update && apk upgrade
# RUN apk add --no-cache libpq-dev gcc
RUN apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# create a directory for the application
RUN mkdir /app
WORKDIR /app

# copy files and install requirements
COPY ./requirements requirements
RUN pip install --no-cache -r requirements/development.txt
COPY . .
RUN apk --purge del .build-deps

# remove carriage return
RUN chmod +x start.sh
RUN sed -i 's/\r$//g' start.sh
RUN chmod +x wait_for_postgres.py
RUN sed -i 's/\r$//g' wait_for_postgres.py

# add new user and make it as default user
RUN addgroup -S appgroup && adduser -D appuser -G appgroup
USER appuser


EXPOSE 5000

RUN ls -ln

ENTRYPOINT ["sh", "/app/start.sh" ]
