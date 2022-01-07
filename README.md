# Demo
The app is deployed to https://young-caverns-47466.herokuapp.com
Rudimentary API docs are found here: https://young-caverns-47466.herokuapp.com/swagger-ui/

# Installation

## Prerequisites
- poetry installed
- Python 3.9 installed
- Postgresql 13+ installed

## Setup

### Create development Postgres DB and user
```
sudo su postgres
psql
create database docmngr_development;
create user docmngr_development with encrypted password 'docmngr';
alter user docmngr_development set timezone to 'UTC';
alter user docmngr_development set client_encoding to 'utf8';
alter user docmngr_development createdb;
\q
exit
```

### Install dependencies:
```
poetry install
```

## Deploying
```
poetry export -f requirements.txt --output requirements.txt
<commit changes>
heroku run python manage.py migrate
git push heroku main
```

## Running migrations remotely

## Requirements
### Use Cases
- Get a folder along with its children *
- Create a folder *
- Delete a folder (only if empty)
- Rename a folder *
- Create a document *
- Get a specific document *
- Move a document to a different folder *
- Create a topic *
- Get a list of all topics
- Add a document to a topic *
- Remove a document from a topic *
- Get all the documents for a topic

# Parting Thoughts
There's a few things I feel are questionable about this implementation:
- The API design is probably not as convenient as it needs to be, or performant. For instance it might be better just to return the whole folder hierarchy in one call rather than expect the client to navigate through it level-by-level.
- I used the pretty low-level `APIView` and `@api_view` which might not have resulted in the cleanest or idiomatic of code. For instance I reimplemented some features of `GenericAPIView.` I did this b/c I haven't done DRF or for that matter any API development from scratch in a long while, so wasn't really confident I could get up to speed on optimally using DRF facilities. Given more time I'd find some production code bases to study and understand best usage of the higher level abstractions like `ViewSet`s and `GenericAPIView`.
- On the same note, I'm pretty sure I did not do the urls.py paths in the most DRY way.
