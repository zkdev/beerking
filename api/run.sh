#!/bin/bash
sudo docker run --name=beerking-api -v beerking-certs:/certs -v beerking-database:/database --detach -p 5000:5000 beerking-api
