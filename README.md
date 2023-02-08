# README

## Objective

Your assignment is to implement a URL shortening service using Python and any framework.

### Brief

ShortLink is a URL shortening service where you enter a URL such as https://codesubmit.io/library/react and it returns a short URL such as http://short.est/GeAi9K.

### Tasks

-   Implement assignment using:
    -   Language: **Python**
    -   Framework: **any framework**
    -   Two endpoints are required
        -   /encode - Encodes a URL to a shortened URL
        -   /decode - Decodes a shortened URL to its original URL.
    -   Both endpoints should return JSON
-   There is no restriction on how your encode/decode algorithm should work. You just need to make sure that a URL can be encoded to a short URL and the short URL can be decoded to the original URL. 

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

## HOWTO

### Requirements

 * Python3
 * Pipenv 

### Getting Started
```
> cd project-directory
> pipenv install
> pipenv shell
> pytest
================================== test session starts ==================================
platform darwin -- Python 3.10.7, pytest-7.2.1, pluggy-1.0.0
rootdir: /Users/gregory.damiani/src/url-shortener
collected 3 items

test_flask.py ...                                                                 [100%]

=================================== 3 passed in 0.15s ===================================
```

### Running As A Basic Service in Test
```
> cd project-directory
> pipenv install
> pipenv shell
> flask --app main run --host=0.0.0.0 0--port=8080
...
> curl localhost:8080/encode/google.com
{"encode":"google.com","result":"8I3R1Z001"}
> curl localhost:8080/decode/8I3R1Z001
{"decode":"8I3R1Z001","result":"google.com"}
```
