#!/bin/bash

if [[ -z $ISOD_LOGIN || -z $ISOD_PASSWORD ]]; then
  echo "Login and/or password not provided. Skipping vpn connection"
  docker-compose up -d
  exit 0
fi

if [[ -z $AUTH_GROUP ]]; then
  export AUTH_GROUP="PWEE - Split"
fi

if [[ -z $VPN_ADDRESS ]]; then
  export VPN_ADDRESS="https://vpn.ee.pw.edu.pl/"
fi

echo "Starting containers"
docker-compose up -d

#echo "Connecting to vpn"
#docker exec ppdv_dash bash ./vpn_connect.sh &