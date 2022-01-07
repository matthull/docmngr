# Installation

## Prerequisites
- poetry installed
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
- Add a document to a topic
- Get all the documents for a topic

### Out of Scope
#### Document history
It seems likely that users will make mistakes and need to roll back to previous document versions,
but this seemed a little complicated to including in a code challenge.

## Caveats

### Performance
#### Token Authentication
This prototype uses DRF native token authentication which causes database lookups. This is bad juju when operating at non-trivial scale. JWT is probably the more correct solution.

I stuck with DRF tokens for this prototype because it saves a good bit of effort on test development as properly generating JWT tokens in tests is non-trivial.

#### Maintainability
This prototype uses monolithic files e.g. `models.py` for all DB models, `serializers.py`, etc. This doesn't scale well for an "real" production app being maintained long term, but it's easy enough to reorganize later so I tend to use monolithic approach when prototyping absent some established structural conventions.

#### Database Migrations
I used Django's builtin DB migration facility, but have concerns about using it when scaling a company. It can produce migrations that cause outages e.g. creating an index non-concurrently. 

It may be better to use a standalone migration system like flyway where migrations are explicitly defined in SQL to encourage mindfulness around migrations. Using the Django built in facilities has big maintainability benefits especially when scaling a team, but a non-standard solution like flyway can pay for the reduced ease of development by preventing service disruptions.

# Notes
- make sure to test unicode anywhere it needs to be supported: folder name, doc name, etc.
