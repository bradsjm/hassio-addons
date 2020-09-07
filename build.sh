#!/bin/sh

docker run --rm -ti --name hassio-builder --privileged \
  -v $(PWD)/addon-hyperion-ng:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  homeassistant/amd64-builder \
  -t /data \
  -i hyperion-ng-addon-{arch} \
  -d bradsjm \
  --all \
  --test
