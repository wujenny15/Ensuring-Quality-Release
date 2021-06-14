#!/bin/bash

# Run JMeter Docker image with options

NAME="jmetertest"
IMAGE="justb4/jmeter:latest"
ROOTPATH=$1

echo "$ROOTPATH"
# Finally run
# The 1 denotes standard output (stdout). The 2 denotes standard error (stderr).
# So 2>&1 says to send standard error to where ever standard output is being redirected as well. 
# Which since it's being sent to /dev/null is akin to ignoring any output at all.
# > means truncate and write
# docker stop one or more running containers
docker stop $NAME > /dev/null 2>&1
docker rm $NAME > /dev/null 2>&1
docker run --name $NAME -i -v $ROOTPATH:/test -w /test $IMAGE ${@:2}