#!/bin/bash
sudo docker run --name=beerking-backend -v beerking-database:/database --detach -p 5000:5000 beerking-backend

