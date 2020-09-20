#!/bin/sh
set -e
ARCH=$1

docker run --rm --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v ${GITHUB_WORKSPACE}/addon-hyperion-ng:/data \
    homeassistant/${ARCH}-builder \
    --target /data \
    --no-cache \
    --docker-user "${DOCKER_USER}" \
    --docker-password "${DOCKER_PASSWORD}" \
    --docker-hub-check \
    --${ARCH}
