#!/bin/sh
ADDON=$1
ARCH=$2

docker run --rm --privileged \
  -v $(PWD)/${ADDON}:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  homeassistant/amd64-builder \
  -t /data \
  -i ${ADDON}-{arch} \
  -d bradsjm \
  --test \
  --${ARCH}
