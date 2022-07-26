# alpine is know as the most lightweight os, suitable for development
FROM python:3.10.4-alpine

# add packages for psycopg2
RUN apk update && apk upgrade
# RUN apk add --no-cache libpq-dev gcc
RUN apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

ARG BUILD_TARGET
ARG TARGET_PORT
ARG COMMAND
ARG ENTRYPOINT

RUN echo "$BUILD_TARGET"
RUN echo "$TARGET_PORT"
RUN echo "$COMMAND"
RUN echo "$ENTRYPOINT"

WORKDIR /srv

# copy files and install requirements
COPY ./requirements requirements
RUN if [ "$BUILD_TARGET" = "production" ] ; then \
    pip install --no-cache -r requirements/production.txt; else \
    pip install --no-cache -r requirements/development.txt;  \
    fi

# remove carriage return
COPY ${ENTRYPOINT} entrypoint.sh
RUN chmod +x entrypoint.sh
RUN sed -i 's/\r$//g' entrypoint.sh

COPY ${COMMAND} command.sh
RUN chmod +x command.sh
RUN sed -i 's/\r$//g' command.sh

COPY wait_for_postgres.py wait_for_postgres.py
COPY config.py config.py
COPY run.py run.py
COPY pytest.ini pytest.ini

RUN mkdir app
COPY app/ app/
COPY migrations/ migrations/
RUN apk --purge del .build-deps

# add new user and make it as default user
RUN addgroup -S appgroup && adduser -D appuser -G appgroup
RUN chown -R appuser:appgroup /srv/
USER appuser

EXPOSE "$TARGET_PORT"

ENTRYPOINT ["sh", "/srv/entrypoint.sh" ]

CMD ["sh", "/srv/command.sh" ]

RUN ls -ln
