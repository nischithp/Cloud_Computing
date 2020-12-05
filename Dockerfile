# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8
RUN mkdir /app
WORKDIR /app/
ADD . /app/
RUN pip install -r requirements.txt
CMD ["python","/app/main.py"]

# Allow statements and log messages to immediately appear in the Cloud Run logs
# ENV PYTHONUNBUFFERED True
# ENV PORT 8080
# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
# COPY requirements.txt ./

# Install production dependencies.
# RUN pip install gunicorn
# RUN pip install -r requirements.txt

# Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# Run the web service on container startup.
# Use gunicorn webserver with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app


# -------------------------------------------------------------------------------------------
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
# FROM python:3.8-slim

# Copy local code to the container image.
# ENV APP_HOME /app
# ENV PORT = 8080
# WORKDIR $APP_HOME
# COPY . ./

# Install production dependencies.
# RUN pip install gunicorn
# RUN pip install -r requirements.txt


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app

# last arguement - <name of main file to be run>:<variable name in app>