# Write a Dockerfile to run the url_shortener inside a containner

# Use a full-featured (bloated) ubuntu container for ease of development
FROM ubuntu:jammy as build

# We're going to run the app as a non-root user
ARG USERNAME=nonroot
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG USER_HOME=/home/$USERNAME

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -d $USER_HOME -m $USERNAME

# Setup python env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv and compilation dependencies
RUN apt-get update && \
    apt-get install --yes gcc python3 python3-pip

# Having some issues with the request or urllib library in this container
RUN pip uninstall requests urllib3 pipenv
RUN pip install requests urllib3 pipenv

# Install our pipenv into its home directory
USER $USERNAME
WORKDIR $USER_HOME
COPY Pipfile .
COPY Pipfile.lock .
COPY main.py .

RUN pipenv install --deploy

## Run the application
ENTRYPOINT ["/usr/local/bin/pipenv", "run", "gunicorn", "--chdir", "/home/nonroot/", "main:app", "-w", "1", "--log-level", "ERROR", "--bind", "0.0.0.0:8000"]
