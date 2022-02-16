# Cesar Australia Web API 

## Development notes

New get request can be added to the `api_blueprint.py` script. The new get request should also be added to the `static/openapi.json` file. To do so, visit [editor.swagger.io](https://editor.swagger.io/#) website and edit the YAML file and convert it JASON when done.

## Containerisation
To containerise the app:
* write a Dockerfile and copy all the files to the docker image
* build the image and run a container
* create a docker network with a subnet by:
```bash
docker network create --subnet 172.20.0.0/16 apinetwork
```
* add PostgreSQL container to the network
```bash
docker network connect --ip 172.20.0.5 apinetwork postgrescontainer
```
* add the api container to the docker network
```bash
docker network connect apinetwork apicontainter
```
* check that both containers are added to the docker network
```bash
docker network inspect apinetwork
```

See [here](https://dev.to/rizkyrajitha/connect-api-and-a-database-with-docker-network-299g) for more details.

## API on AWS server
* pull the API docker image and run on the EC2 server
* replace the database password
* create a docker network in docker compose
* add both API and PostgreSQL containers to the network
* make sure the port 5000 is accessible from the EC2 instance.