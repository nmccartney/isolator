FROM python:3.9-slim as builder

WORKDIR /flask-api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install libgl1 libglib2.0-0 -y
RUN apt-get install -y ffmpeg 
RUN apt-get install -y libsndfile1
RUN apt-get install -y curl
# RUN apt-get --yes install libsndfile1

COPY requirements.txt .


# install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --root-user-action=ignore --no-cache-dir -r requirements.txt

RUN pip3 install celery
RUN pip3 install spleeter
# COPY ./gunicorn-cfg.py .
COPY . .

# Cache is invalidated when ARG is USED so put this low in stage
ARG BUILD_DATE
ENV BUILD_DATE="$BUILD_DATE"
ARG GIT_HASH
ENV GIT_HASH="$GIT_HASH"
ARG GIT_TAG=""
ENV GIT_TAG="$GIT_TAG"
ARG BUILD_TYPE=
ENV BUILD_TYPE="$BUILD_TYPE"

# Set the environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

EXPOSE 5000


# FROM builder as dev
# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]



FROM builder as watch-dev

COPY --from=builder /flask-api /flask-api

WORKDIR /flask-api

# ENTRYPOINT python ./run.py
