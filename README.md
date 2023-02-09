# README

## HOWTO

### Requirements

 * Python3
 * Pipenv 

### Quickstart

I've included a simple Makefile in this directory. The default build target builds and runs the project in a Docker container, mapping localhost:8000 to the listening port of the service. As a last verification step, make curls that endpoint and should display the default response:
```
> make
...
[+] Building 0.1s (13/13) FINISHED
...
Hello, Url Shortener%
```

We can quickly verify the three endpoints work like so:
```
> curl localhost:8000
Hello, Url Shortener%

> curl -X POST "localhost:8000/encode?url=https://www.finn.com"
{"encode":"https://www.finn.com","result":"LTJ0U4YHM"}

> curl -X GET localhost:8000/decode/LTJ0U4YHM
{"decode":"LTJ0U4YHM","result":"https://www.finn.com"}
```

### Running pytest
```
> cd project-directory
> pipenv install
> pipenv shell
> pytest --verbose
================================ test session starts ================================
platform darwin -- Python 3.10.7, pytest-7.2.1, pluggy-1.0.0 -- /Users/gregory.damiani/.local/share/virtualenvs/url-shortener-GAw33Mzq/bin/python
cachedir: .pytest_cache
rootdir: /Users/gregory.damiani/src/url-shortener
collected 7 items

test_flask.py::test_get_root_url PASSED                                       [ 14%]
test_flask.py::test_encode_url PASSED                                         [ 28%]
test_flask.py::test_key_not_found PASSED                                      [ 42%]
test_flask.py::test_decode_id PASSED                                          [ 57%]
test_flask.py::test_encode_challenging_url PASSED                             [ 71%]
test_flask.py::test_bad_urls PASSED                                           [ 85%]
test_flask.py::test_bad_methods PASSED                                        [100%]

================================= 7 passed in 0.25s =================================

### Running As A Basic Service in Test
```
> cd project-directory
> pipenv install
> pipenv shell
> flask --app main run --host=0.0.0.0 --port=8080
...
> curl -X POST "localhost:8080/encode?url=https://www.google.com/search?q=finn+gmbh"
{"encode":"https://www.google.com/search?q=finn gmbh","result":"GGE71A20B"}
> curl -X GET localhost:8080/decode/GGE71A20B
{"decode":"GGE71A20B","result":"https://www.google.com/search?q=finn gmbh"}
```

### Running inside gunicorn
Let's run our flask api inside gunicorn for speed and stability. We can only safely use on worker at the moment, because all shortened urls are stored in local memory. Once we move the URL storage to a shared database, we can increase the gunicorn workers as much as we want, only limited by the amount of memory we have available.
```
> cd project-directory
> pipenv install
> pipenv shell
> gunicorn -w 1 --log-level DEBUG --bind 0.0.0.0:8080 'main:app'
...
```

### Running in Docker
```
> cd project-directory
> docker build -t url .
[+] Building 0.1s (15/15) FINISHED
 => [internal] load build definition from Doc  0.0s
 => => transferring dockerfile: 1.20kB         0.0s
 => [internal] load .dockerignore              0.0s
 => => transferring context: 2B                0.0s
 => [internal] load metadata for docker.io/li  0.0s
 => [internal] load build context              0.0s
 => => transferring context: 88B               0.0s
 => [ 1/10] FROM docker.io/library/ubuntu:jam  0.0s
 => CACHED [ 2/10] RUN groupadd --gid 1000 no  0.0s
 => CACHED [ 3/10] RUN apt-get update &&       0.0s
 => CACHED [ 4/10] RUN pip uninstall requests  0.0s
 => CACHED [ 5/10] RUN pip install requests u  0.0s
 => CACHED [ 6/10] WORKDIR /home/nonroot       0.0s
 => CACHED [ 7/10] COPY Pipfile .              0.0s
 => CACHED [ 8/10] COPY Pipfile.lock .         0.0s
 => CACHED [ 9/10] COPY main.py .              0.0s
 => CACHED [10/10] RUN pipenv install --deplo  0.0s
 => exporting to image                         0.0s
 => => exporting layers                        0.0s
 => => writing image sha256:91d5dc3be44255013  0.0s
 => => naming to docker.io/library/url         0.0s

> docker run -p 8000:8000 url &
[1] 18055

> curl localhost:8000
Hello, Url Shortener%

> curl -X POST "localhost:8000/encode?url=https://www.google.com/search?q=finn"
{"encode":"https://www.google.com/search?q=finn","result":"FEITCMXLM"}

> curl -X GET localhost:8000/decode/FEITCMXLM
{"decode":"FEITCMXLM","result":"https://www.google.com/search?q=finn"}

### Multi-stage build
```
> docker images url
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
url          latest    200e68033171   11 minutes ago   549MB
```

Let's see if we can make a multi-stage build to decrease the size of the image while we decrease the attack surface inside the running container.

Starting from the following base image, creating the nonroot user, and running the app from $HOME yielded positive results:
```
FROM python:3.10-slim AS runnable
```

As seen here, we've improved the container size by more than 60%:
```
> docker images url
REPOSITORY   TAG       IMAGE ID       CREATED              SIZE
url          latest    0a38d237c812   About a minute ago   209MB
```


## TODO

 * -pylint, python best practices, dir structure-
 * security checks
 * -multistage or distroless docker build-
 * admin interface to list all stored/shortened urls
 * k8s config
 * better logging
 * figure out why the url shortener can't handle "+" characters

## Objective

Your assignment is to implement a URL shortening service using Python and any framework.

### Brief

ShortLink is a URL shortening service where you enter a URL such as https://codesubmit.io/library/react and it returns a short URL such as http://short.est/GeAi9K.

### Tasks

 - Implement assignment using:
   - Language: **Python**
   - Framework: **any framework**
   - Two endpoints are required
     -   /encode - Encodes a URL to a shortened URL
     -   /decode - Decodes a shortened URL to its original URL.
   - Both endpoints should return JSON
 - There is no restriction on how your encode/decode algorithm should work. You just need to make sure that a URL can be encoded to a short URL and the short URL can be decoded to the original URL. 

**You do not need to persist short URLs to a database. Keep them in memory.**

-   Provide detailed instructions on how to run your assignment in a separate markdown file
-   Provide API tests for both endpoints

### Evaluation Criteria

-   **Python** best practices
-   API implemented featuring a /encode and /decode endpoint
-   Show us your work through your commit history
-   Completeness: did you complete the features? Are all the tests running?
-   Correctness: does the functionality act in sensible, thought-out ways?
-   Maintainability: is it written in a clean, maintainable way?


### CodeSubmit

Please organize, design, test and document your code as if it were going into production - then push your changes to the master branch. After you have pushed your code, you may submit the assignment on the assignment page.

All the best and happy coding,

