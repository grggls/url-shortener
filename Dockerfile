# Write a Dockerfile to run the url_shortener inside a containner

# Use a start with a slim, kinda distroless container image
FROM python:3.10-slim AS runnable

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

# Setup our home directory and install our pipenv
USER $USERNAME
WORKDIR $USER_HOME
COPY Pipfile .
COPY Pipfile.lock .
COPY main.py .

RUN pip install pipenv
ENV PATH="$USER_HOME/.local/bin:$PATH"
RUN pipenv install --deploy

## Run the application
ENTRYPOINT ["pipenv", "run", "gunicorn", "--chdir", "/home/nonroot/", "main:app", "-w", "1", "--log-level", "ERROR", "--bind", "0.0.0.0:8000"]
