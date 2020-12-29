#!/bin/bash

printf "$ISOD_PASSWORD\n" | openconnect -u $ISOD_LOGIN --passwd-on-stdin --authgroup "$AUTH_GROUP" "$VPN_ADDRESS"