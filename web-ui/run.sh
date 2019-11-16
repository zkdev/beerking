#!/bin/bash
sudo docker run --name=beerking-web-ui -v beerking-certs:/certs --detach -p 6669:6669 beerking-web-ui
