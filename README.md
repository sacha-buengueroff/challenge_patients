# Light-It Challenge
## Setup development environment

Please install Docker and Docker compose first.

https://www.docker.com/

After installation, run the following command to create a local Docker container.

```
docker-compose build
docker-compose up
```

If Docker is running successfully, the API and DB server will be launched as shown in the following:

- API server: http://localhost:8080
- MYSQL server: http://localhost:3306

You can check the Swagger docs of the API by going to the following URL: http://localhost:8080/docs

## Testing

Once the Docker container is running succesfuly you can run the following command to test the app.

In this project we created a dependency override to avoid writing to the db while testing.

Normally I would have another db only for the testing environment so data isn't corrupted.
```
docker exec -i app bash -c "cd project && pytest"
```
