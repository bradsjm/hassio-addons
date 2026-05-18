#!/bin/sh
set -e
ARCH=$1
DOCKER_ARGS=""
BUILDER_ARGS=""

if [ "${TEST_MODE:-false}" = "true" ]; then
    BUILDER_ARGS="--test"
fi

if [ -n "${DOCKER_USER:-}" ] && [ -n "${DOCKER_PASSWORD:-}" ]; then
    DOCKER_ARGS="--docker-user ${DOCKER_USER} --docker-password ${DOCKER_PASSWORD}"
fi

docker run --rm --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v ${GITHUB_WORKSPACE:-$(PWD)}/addon-mcpx:/data \
    homeassistant/amd64-builder \
    --target /data \
    ${DOCKER_ARGS} \
    ${BUILDER_ARGS} \
    --no-latest \
    --${ARCH:-all}
