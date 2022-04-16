# alpine is know as the most lightweight os, suitable for development
FROM python:3.10.4-alpine

# create a directory for the application
RUN mkdir /app
WORKDIR /app

# copy files and install requirements
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# remove carriage return
RUN chmod +x start.sh
RUN sed -i 's/\r$//g' start.sh

# add new user and make it as default user 
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 5000

RUN ls -ln

ENTRYPOINT ["sh", "/app/start.sh" ]