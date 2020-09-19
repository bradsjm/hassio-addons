#!/bin/sh
set -e

docker run --rm --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v ${GITHUB_WORKSPACE}/addon-hyperion-ng:/data \
    homeassistant/amd64-builder \
    --target /data \
    --no-cache \
    --docker-user "${DOCKER_USER}" \
    --docker-password "${DOCKER_PASSWORD}" \
    --docker-hub-check \
    --$1
