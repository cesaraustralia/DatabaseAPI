# Cesar Australia Web API 

## Development notes

New get request can be added to the `app.py` script. The new get request should also be added to the `static/openapi.json` file. To do so, visit [editor.swagger.io](https://editor.swagger.io/#) website and edit the YAML file and convert it JASON when done.

## Containerisation
To containerise the app:
* copy all the files in the docker image and run the app
* build the image and run a container
* create a docker network with a subnet by:
```bash
docker network create --subnet 172.20.0.0/16 apinetwork
```
* add PostgreSQL container to the network
```bash
docker network connect --ip 172.20.0.5 apinetwork postgrecontainer
```
* add the api container to the docker network
```bash
docker network connect apinetwork apicontainter
```

See [here](https://dev.to/rizkyrajitha/connect-api-and-a-database-with-docker-network-299g) for more details.

## API on AWS server
Add pull the API docker iamge and run on the EC2 server. Create a docker network and add both API and PostgreSQL containers to the network.