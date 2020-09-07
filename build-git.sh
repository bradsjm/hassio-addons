#!/bin/sh

docker run --rm  --name hassio-builder--privileged \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v ~/.docker:/root/.docker homeassistant/amd64-builder \
  -r https://github.com/bradsjm/hassio-addons \
  -b master \
  -t addon-hyperion-ng \
  --docker-user bradsjm \
  --docker-password ${PASSWORD} \
  --all