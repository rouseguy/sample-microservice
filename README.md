To start microservice, first we need to create a docker image:
```
docker build -t sample-service-image -f Dockerfile.sample-service .
```

Then start the container by using docker-compose:
```
docker-compose -f docker-compose-sample-service.yml up sample-service
```

To test the service: 
```
curl http://127.0.0.1:5001/
```
