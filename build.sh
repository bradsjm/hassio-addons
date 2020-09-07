#!/bin/sh

docker run --rm -ti --name hassio-builder --privileged \
  -v $(PWD)/hyperion-ng:/data \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  homeassistant/amd64-builder -t /data --all --test \
  -i hyperion-ng-addon-{arch} -d local
