# django-simple-api
REST api for management users and their resources

---------------------------------

## Methods    

Endpoint | HTTP Method | Only admin | Result
-- | -- | -- | --
`users` | GET | ✅ | Get list users
`users` | POST | ✅ | Create user
`users/<user_id>` | DELETE | ✅ | Delete user by id
`users/resources`| GET | ❌ | Get list resources authenticated user
`users/resources`| POST | ❌ | Create resource authenticated user
`users/<user_id>/resources`| GET | ❌ | Get list resources by user_id
`users/<user_id>/resources`| POST | ❌ | Create resource by user_id
`users/<user_id>/resources/<resource_id>`| DELETE | ❌ | Delete resource by user_id and resource_id
`users/<user_id>/quota`| PATCH | ✅ | Set quota by user_id
`token/` | POST  | ❌ | Get a token for authentication


## How use token

Pipeline for authentication:

1. Get a access token:
```
curl \
    -d '{"email": <email>, "password": <password>}' \
    -H "Content-Type: application/json" \
    -X POST http://<host>:<port>/api/token/
```
2. Use any methods with got access token:
```
 curl \
    -H "Authorization: Bearer <token.access>" \
    -H "Content-Type: application/json"\
    ...
```


## Difference between user and administrator (or superuser)

* User can:
    1. management only personal resources

* Administrator can:
    1. management user
    2. management any resources
    3. set quota for count resources for any user

**But administrator also is user**

## Environment Variables
* POSTGRES_HOST

* POSTGRES_PORT

* POSTGRES_USER

* POSTGRES_PASSWORD

* POSTGRES_DB

* SECRET_KEY

* DEBUG: default false


## Run local

1. Create a postgre database

2. Create a Python 3.9 virtualenv:
```
    virtaulenv .venv
```

3. Activate it:
```
    source .venv/bin/activate
```

4. Set environment variables

5. Install requirements:
```
    pip install -r requirements.txt
```

6. Run migration:
```
    python manage.py migrate
```

7. Run server:
```
    python manage.py runserver [host:port]
```


## Run with Docker-Compose
* For running use:
```
docker-compose up
```

If need use personal environment variables in docker-compose.yml


## Running integration tests
* For running integration tests use:
```
docker-compose \
    -f docker-compose.yml \
    -f docker-compose.test.yml \
    up \
    --abort-on-container-exit
```
